import { useEffect, useState } from "react";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import { streamChatResponse } from "@/services/chatService";

const createSession = (title = "New Chat") => ({
  id:
    typeof crypto !== "undefined" && crypto.randomUUID
      ? crypto.randomUUID()
      : `session-${Date.now()}`,
  title,
  messages: [],
});

const ChatBox = () => {
  const [sessions, setSessions] = useState(() => [createSession()]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!activeSessionId && sessions.length > 0) {
      setActiveSessionId(sessions[0].id);
    }
  }, [activeSessionId, sessions]);

  const activeSession = sessions.find((session) => session.id === activeSessionId) || sessions[0];

  const createNewSession = () => {
    const newSession = createSession();
    setSessions((prev) => [newSession, ...prev]);
    setActiveSessionId(newSession.id);
  };

  const sendMessage = async (text) => {
    if (!activeSession) return;

    setLoading(true);

    const userMessage = {
      role: "user",
      content: text,
    };

    const assistantIndex = activeSession.messages.length + 1;
    const title = activeSession.title === "New Chat"
      ? text.trim().slice(0, 40) || "New Chat"
      : activeSession.title;

    setSessions((prev) =>
      prev.map((session) => {
        if (session.id !== activeSession.id) return session;

        return {
          ...session,
          title,
          messages: [
            ...session.messages,
            userMessage,
            {
              role: "assistant",
              content: "",
            },
          ],
        };
      })
    );

    let assistantText = "";

    await streamChatResponse({
      message: text,
      threadId: activeSession.id,

      onToken: (token) => {
        assistantText += token;

        setSessions((prev) =>
          prev.map((session) => {
            if (session.id !== activeSession.id) return session;

            const updatedMessages = [...session.messages];
            updatedMessages[assistantIndex] = {
              role: "assistant",
              content: assistantText,
            };

            return {
              ...session,
              messages: updatedMessages,
            };
          })
        );
      },

      onToolStart: (tool) => {
        console.log("Tool called:", tool);
      },

      onError: (error) => {
        console.error(error);
        setLoading(false);
      },
    });

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 px-2 py-3 sm:px-4 sm:py-4">
      <div className="mx-auto flex h-[calc(100vh-3.5rem)] max-w-6xl overflow-hidden rounded-xl border border-slate-200 bg-white shadow-[0_25px_80px_rgba(15,23,42,0.08)]">
        <aside className="flex w-80 flex-col border-r border-slate-200 bg-slate-50/80 p-3">
          <div className="mb-3 flex items-center justify-between gap-2">
            <div>
              <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Chats</p>
              <h4 className="text-base font-semibold text-slate-900">AI Assistant</h4>
            </div>
            <button
              type="button"
              onClick={createNewSession}
              className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-700 shadow-sm transition hover:border-slate-300 hover:bg-slate-100"
            >
              New chat
            </button>
          </div>

          <div className="flex-1 space-y-2 overflow-y-auto">
            {sessions.map((session) => (
              <button
                key={session.id}
                type="button"
                onClick={() => setActiveSessionId(session.id)}
                className={`w-full rounded-xl border p-3 text-left transition ${
                  session.id === activeSessionId
                    ? "border-sky-200 bg-sky-50 shadow-sm"
                    : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-100"
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="truncate text-sm font-semibold text-slate-900">{session.title}</span>
                  <span className="text-[11px] text-slate-500">{session.messages.length} msgs</span>
                </div>
                <p className="mt-1 line-clamp-2 text-xs text-slate-500">
                  {session.messages.length > 0
                    ? session.messages[session.messages.length - 1].content || "..."
                    : "Start a new conversation in this thread."}
                </p>
              </button>
            ))}
          </div>
        </aside>

        <main className="flex min-w-0 flex-1 flex-col">
          <div className="border-b border-slate-200 p-3 text-center">
            <h4 className="text-base font-semibold text-slate-900">{activeSession?.title || "AI Assistant ChatBot"}</h4>
            <p className="text-xs text-slate-500">Each chat session uses its own thread ID for independent history.</p>
          </div>

          <MessageList messages={activeSession?.messages || []} />

          <MessageInput loading={loading} onSend={sendMessage} />
        </main>
      </div>
    </div>
  );
};

export default ChatBox;