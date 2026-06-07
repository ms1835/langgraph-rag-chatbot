
const ChatMessage = ({ message }) => {
  const isUser = message.role === "user";

  return (
    <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`rounded-3xl px-3 py-2 max-w-[80%] whitespace-pre-wrap text-xs leading-5 ${isUser ? "bg-blue-600 text-white" : "bg-slate-100 text-slate-900"}`}
      >
        {message.content}
      </div>
    </div>
  );
}

export default ChatMessage;