import { useState, useEffect } from "react";
import { createInteraction } from "../api/interactionApi";
import InteractionList from "./InteractionList";

const initialFormData = {
  hcp_name: "",
  interaction_type: "",
  interaction_date: "",
  topics_discussed: "",
  materials_shared: "",
  samples_distributed: "",
  sentiment: "",
  outcome: "",
  follow_up_action: "",
  summary: "",
};


function InteractionForm({ aiData , refreshTrigger, onInteractionSaved }) {
  
  const [formData, setFormData] = useState(initialFormData);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");


  
  const handleChange = (e) => {
  const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  useEffect(() => {
  if (aiData && Object.keys(aiData).length > 0) {
    setFormData((prev) => ({
      ...prev,
      ...aiData,
    }));
  }
}, [aiData]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const savedInteraction = await createInteraction(formData);
      setMessage(`Interaction saved successfully. ID: ${savedInteraction.id}`);
      setFormData(initialFormData);
      onInteractionSaved();
    } catch (error) {
      console.error(error);
      setMessage("Failed to save interaction.");
    } finally {
      setLoading(false);
    }
  };


  
    return (
        <>
     <form onSubmit={handleSubmit} className="space-y-4">
      <input
        name="hcp_name"
        value={formData.hcp_name}
        onChange={handleChange}
        placeholder="HCP Name"
        className="w-full rounded-xl border border-gray-300 px-4 py-3"
        required
      />

      <select
        name="interaction_type"
        value={formData.interaction_type}
        onChange={handleChange}
        className="w-full rounded-xl border border-gray-300 px-4 py-3"
        required
      >
        <option value="">Select Interaction Type</option>
        <option value="In-person Meeting">In-person Meeting</option>
        <option value="Phone Call">Phone Call</option>
        <option value="Email">Email</option>
        <option value="Virtual Meeting">Virtual Meeting</option>
      </select>

      <input
        type="date"
        name="interaction_date"
        value={formData.interaction_date}
        onChange={handleChange}
        className="w-full rounded-xl border border-gray-300 px-4 py-3"
        required
      />

      <textarea
        name="topics_discussed"
        value={formData.topics_discussed}
        onChange={handleChange}
        placeholder="Topics Discussed"
        className="w-full rounded-xl border border-gray-300 px-4 py-3 min-h-24"
      />

      <textarea
        name="materials_shared"
        value={formData.materials_shared}
        onChange={handleChange}
        placeholder="Materials Shared"
        className="w-full rounded-xl border border-gray-300 px-4 py-3 min-h-20"
      />

      <textarea
        name="samples_distributed"
        value={formData.samples_distributed}
        onChange={handleChange}
        placeholder="Samples Distributed"
        className="w-full rounded-xl border border-gray-300 px-4 py-3 min-h-20"
      />

      <select
        name="sentiment"
        value={formData.sentiment}
        onChange={handleChange}
        className="w-full rounded-xl border border-gray-300 px-4 py-3"
      >
        <option value="">Select Sentiment</option>
        <option value="Positive">Positive</option>
        <option value="Neutral">Neutral</option>
        <option value="Negative">Negative</option>
      </select>

      <textarea
        name="outcome"
        value={formData.outcome}
        onChange={handleChange}
        placeholder="Outcome"
        className="w-full rounded-xl border border-gray-300 px-4 py-3 min-h-20"
      />

      <textarea
        name="follow_up_action"
        value={formData.follow_up_action}
        onChange={handleChange}
        placeholder="Follow-up Action"
        className="w-full rounded-xl border border-gray-300 px-4 py-3 min-h-20"
      />

      <textarea
        name="summary"
        value={formData.summary}
        onChange={handleChange}
        placeholder="Summary"
        className="w-full rounded-xl border border-gray-300 px-4 py-3 min-h-20"
      />

      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-xl bg-blue-600 text-white py-3 font-semibold hover:bg-blue-700 disabled:bg-blue-300"
      >
        {loading ? "Saving..." : "Save Interaction"}
      </button>

      {message && (
        <p className="text-sm text-gray-600">
          {message}
        </p>
      )}
    </form>
    <InteractionList refreshTrigger={refreshTrigger} />
    </>
  );
}

export default InteractionForm;