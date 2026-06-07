import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";

const MessageList = ({ messages }) => {
  const bottomRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [messages]);

  return (
    <div className="flex-1 min-h-0 overflow-y-auto px-4 py-3 sm:px-5 sm:py-4 space-y-3">
      {messages.map((message, index) => (
        <ChatMessage key={index} message={message} />
      ))}

      <div ref={bottomRef} />
    </div>
  );
}

export default MessageList;