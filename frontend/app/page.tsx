"use client";

import { FormEvent, useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

const initialMessages: Message[] = [
  {
    role: "assistant",
    content: "I can investigate delayed shipments, inventory shortages, and carrier exceptions.",
  },
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [query, setQuery] = useState(
    "Order ORD123 was supposed to arrive yesterday but it has not arrived. What should we do?"
  );
  const [orderId, setOrderId] = useState("ORD123");
  const [status, setStatus] = useState("Ready");
  const [agentState, setAgentState] = useState("Triage → Data → Policy → Investigation → Recovery");
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setStatus("Running workflow");
    setMessages((current) => [...current, { role: "user", content: query }]);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_query: query, order_id: orderId, user_id: "ops-user" }),
      });
      const payload = await response.json();
      setResult(payload);
      setStatus("Completed");
      setAgentState("Complete");
      setMessages((current) => [
        ...current,
        { role: "assistant", content: payload.final_response ?? "No result generated." },
      ]);
    } catch (error) {
      setStatus("Error contacting backend");
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: "The backend is not available at the moment. Please confirm the FastAPI service is running.",
        },
      ]);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-7xl p-6">
        <header className="mb-6 flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-cyan-400">Agentic Fulfillment Recovery Planner</p>
            <h1 className="mt-2 text-3xl font-bold">Operations Recovery Console</h1>
          </div>
          <div className="rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-sm text-emerald-300">
            {status}
          </div>
        </header>

        <div className="grid gap-6 lg:grid-cols-[1.5fr_0.9fr]">
          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-semibold">Conversation</h2>
              <span className="text-sm text-slate-400">{agentState}</span>
            </div>

            <div className="space-y-3">
              {messages.map((message, index) => (
                <div
                  key={`${message.role}-${index}`}
                  className={`rounded-xl p-3 ${
                    message.role === "user"
                      ? "ml-10 bg-cyan-500/10 text-cyan-50"
                      : "mr-10 bg-slate-800 text-slate-100"
                  }`}
                >
                  <div className="mb-1 text-[10px] uppercase tracking-[0.2em] text-slate-400">{message.role}</div>
                  <p className="text-sm leading-6">{message.content}</p>
                </div>
              ))}
            </div>

            <form onSubmit={handleSubmit} className="mt-6 space-y-3">
              <label className="block text-sm text-slate-300">
                Order ID
                <input
                  value={orderId}
                  onChange={(event) => setOrderId(event.target.value)}
                  className="mt-1 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 outline-none focus:border-cyan-400"
                />
              </label>
              <label className="block text-sm text-slate-300">
                Request
                <textarea
                  rows={4}
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  className="mt-1 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 outline-none focus:border-cyan-400"
                />
              </label>
              <button
                type="submit"
                className="rounded-xl bg-cyan-500 px-4 py-2 font-medium text-slate-950 transition hover:bg-cyan-400"
              >
                Run Recovery Workflow
              </button>
            </form>
          </section>

          <aside className="space-y-6">
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
              <h3 className="mb-3 text-lg font-semibold">Workflow Panel</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li>• Triage</li>
                <li>• Operational Retrieval</li>
                <li>• Policy Retrieval</li>
                <li>• Investigation</li>
                <li>• Recovery Planning</li>
                <li>• Validation</li>
                <li>• Human Approval</li>
                <li>• Action</li>
                <li>• Response</li>
              </ul>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
              <h3 className="mb-3 text-lg font-semibold">Sources</h3>
              <ul className="text-sm text-slate-300">
                {result?.citations?.length ? (
                  result.citations.map((citation: string, index: number) => (
                    <li key={`${citation}-${index}`}>• {citation}</li>
                  ))
                ) : (
                  <li>• No citations yet</li>
                )}
              </ul>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
              <h3 className="mb-3 text-lg font-semibold">Approval Panel</h3>
              <div className="space-y-2 text-sm text-slate-300">
                <p>Proposed action: {result?.recovery_plan?.actions?.join(", ") ?? "Awaiting plan"}</p>
                <p>Confidence: {result?.recovery_plan?.estimated_confidence ?? "0"}</p>
                <p>Risk: {result?.recovery_plan?.risk_level ?? "unknown"}</p>
              </div>
              <div className="mt-4 flex gap-2">
                <button className="rounded-lg bg-emerald-500 px-3 py-2 text-sm font-medium text-slate-900">Approve</button>
                <button className="rounded-lg bg-rose-500 px-3 py-2 text-sm font-medium text-white">Reject</button>
                <button className="rounded-lg bg-slate-700 px-3 py-2 text-sm font-medium text-white">Modify</button>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </main>
  );
}
