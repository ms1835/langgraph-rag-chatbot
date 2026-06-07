import { useState } from "react";


const MessageInput = ({ onSend, loading }) => {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) 
      return;

    onSend(input);
    setInput("");
  };

  const handleKeyDown = (e) => {
    if ( e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-slate-200 bg-slate-50 p-2 sm:px-4 sm:py-4">
      <div className="flex flex-row gap-2 sm:items-center items-center">
        <textarea
          className="flex-1 min-h-[50px] resize-none rounded-2xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 outline-none placeholder:text-slate-400 focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
          value={input}
          placeholder="Ask something..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        <button
          className="h-11 rounded-2xl bg-blue-600 px-4 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-500 sm:w-auto"
          disabled={loading}
          onClick={handleSend}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default MessageInput;