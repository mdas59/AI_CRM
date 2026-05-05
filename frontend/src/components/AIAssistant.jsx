import { useEffect, useRef, useState } from "react";
import { runAgent } from "../api/interactionApi";

function formatAIResponse(data) {
  if (data.hcp_name !== undefined) {
    return `✅ Interaction parsed for ${data.hcp_name || "Unknown HCP"}.\nClick "Apply to Form" to fill the structured form.`;
  }

  if (data.status === "success") {
    return `✏️ ${data.message}`;
  }

  if (data.follow_up_action) {
    return `📅 Follow-up Suggestion:\n${data.follow_up_action}\n\nReason: ${data.reason || "Based on interaction context."}`;
  }

  if (data.recommended_materials) {
    return `📦 Recommended Materials:\n${data.recommended_materials.join(", ")}\n\nReason: ${data.reason || ""}`;
  }

  if (data.hcp_name && data.lookup_intent) {
    return `🔍 Looking up details for ${data.hcp_name}`;
  }

  return "🤖 Response received.";
}

function AIAssistant({ onFillForm, onInteractionUpdated }) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userInput = input;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userInput,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const data = await runAgent(userInput);

      if (data.status === "success" && data.updated_interaction) {
        onInteractionUpdated();
      }

      const aiMessage = {
        role: "ai",
        content: formatAIResponse(data),
        rawData: data,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: "⚠️ Something went wrong while processing your request.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyToForm = (data) => {
    onFillForm(data);
  };

  const isFormDataResponse = (data) => {
    return data && data.hcp_name !== undefined;
  };

  return (
    <div className="flex flex-col h-full">
      {/* CHAT AREA */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-2">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-xl text-sm whitespace-pre-line ${
              msg.role === "user"
                ? "bg-blue-100 ml-auto max-w-[85%]"
                : "bg-gray-100 mr-auto max-w-[90%]"
            }`}
          >
            <div>{msg.content}</div>

            {msg.role === "ai" && isFormDataResponse(msg.rawData) && (
              <button
                onClick={() => handleApplyToForm(msg.rawData)}
                className="mt-3 rounded-lg bg-blue-600 px-3 py-2 text-xs font-semibold text-white hover:bg-blue-700"
              >
                Apply to Form
              </button>
            )}
          </div>
        ))}

        {/* TYPING ANIMATION */}
        {loading && (
          <div className="bg-gray-100 mr-auto max-w-[90%] p-3 rounded-xl text-sm">
            <div className="flex items-center gap-2">
              <span className="text-gray-500">AI is thinking</span>
              <div className="flex gap-1">
                <span className="h-2 w-2 rounded-full bg-gray-400 animate-bounce"></span>
                <span className="h-2 w-2 rounded-full bg-gray-400 animate-bounce [animation-delay:0.15s]"></span>
                <span className="h-2 w-2 rounded-full bg-gray-400 animate-bounce [animation-delay:0.3s]"></span>
              </div>
            </div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* INPUT AREA */}
      <div className="mt-4 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSend();
            }
          }}
          placeholder="Describe interaction or ask something..."
          className="flex-1 border rounded-xl px-4 py-2"
        />

        <button
          onClick={handleSend}
          disabled={loading}
          className="bg-blue-600 text-white px-4 rounded-xl disabled:bg-blue-300"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default AIAssistant;