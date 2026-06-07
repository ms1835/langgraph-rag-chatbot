import { useState } from "react";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import { streamChatResponse } from "@/services/chatService";

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (text) => {
    setLoading(true);

    const userMessage = {
      role: "user",
      content: text
    };

    // assistant will be the next slot after the new user message
    const assistantIndex = messages.length + 1;

    // Append both the user message and a single assistant placeholder in one update
    setMessages((prev) => [
      ...prev,
      userMessage,
      {
        role: "assistant",
        content: "",
      },
    ]);

    let assistantText = "";

    await streamChatResponse({
      message: text,
      threadId: "1",

      onToken: (token) => {
        assistantText += token;

        setMessages((prev) => {
          const updatedText = [
            ...prev,
          ];

          updatedText[assistantIndex] = {
            role: "assistant",
            content: assistantText
          };

          return updatedText;
        });
      },

      onToolStart: (tool) => {
        console.log("Tool called:", tool);
      },

      onError: (error) => {
        console.error(error);
      },
    });

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 px-2 py-3 sm:px-4 sm:py-4">
      <div className="mx-auto flex h-[calc(100vh-3.5rem)] max-w-3xl flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-[0_25px_80px_rgba(15,23,42,0.08)]">
        <div className="border-b border-slate-200 p-2 justify-center text-center">
          <h4 className="text-base font-semibold text-slate-900">AI Assistant ChatBot</h4>
          {/* <p className="mt-1 text-xs text-slate-500">Only messages scroll below; header and input stay visible.</p> */}
        </div>

        <MessageList messages={messages} />

        <MessageInput
          loading={loading}
          onSend={sendMessage}
        />
      </div>
    </div>
  );
}

export default ChatBox;