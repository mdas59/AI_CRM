import { useState } from "react";
import InteractionForm from "../components/InteractionForm";
import AIAssistant from "../components/AIAssistant";

function LogInteraction() {
  const [aiData, setAiData] = useState({});
  const [refreshTrigger, setRefreshTrigger] = useState(false);

  const refreshInteractions = () => {
    setRefreshTrigger((prev) => !prev);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[90vh]">
        <div className="bg-white rounded-2xl shadow-md p-6 overflow-y-auto">
          <h2 className="text-xl font-semibold mb-4">Log Interaction</h2>

          <InteractionForm
            aiData={aiData}
            refreshTrigger={refreshTrigger}
            onInteractionSaved={refreshInteractions}
          />
        </div>

        <div className="bg-white rounded-2xl shadow-md p-6 flex flex-col">
          <h2 className="text-xl font-semibold mb-4">AI Assistant</h2>

          <AIAssistant
            onFillForm={setAiData}
            onInteractionUpdated={refreshInteractions}
          />
        </div>
      </div>
    </div>
  );
}

export default LogInteraction;