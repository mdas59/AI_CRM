import { useEffect, useState } from "react";
import { getInteractions } from "../api/interactionApi";

function InteractionList({ refreshTrigger }) {
  const [interactions, setInteractions] = useState([]);

  useEffect(() => {
    fetchInteractions();
  }, [refreshTrigger]);

  const fetchInteractions = async () => {
    try {
      const data = await getInteractions();
      setInteractions(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold mb-3">
        Recent Interactions
      </h3>

      <div className="space-y-3 max-h-64 overflow-y-auto">
        {interactions.map((item) => (
          <div
            key={item.id}
            className="border rounded-xl p-4 flex justify-between items-center"
          >
            <div>
              <p className="font-medium">{item.hcp_name}</p>
              <p className="text-sm text-gray-500">
                {item.interaction_type} • {item.interaction_date}
              </p>
            </div>

            <span className="text-sm px-3 py-1 rounded-full bg-gray-100">
              {item.sentiment || "N/A"}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default InteractionList;