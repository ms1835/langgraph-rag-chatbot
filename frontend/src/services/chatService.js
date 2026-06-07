export const streamChatResponse = async ({
  message,
  threadId,
  onToken,
  onToolStart,
  onError,
}) => {
  try {
    const response = await fetch(
      "http://localhost:8000/chat",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
          thread_id: threadId,
        }),
      }
    );

    if (!response.ok) {
      throw new Error("Failed to connect");
    }

    const reader = response.body.getReader();

    const decoder = new TextDecoder();

    let buffer = "";

    while (true) {
      const { done, value } =
        await reader.read();

      if (done) break;

      buffer += decoder.decode(value, {
        stream: true,
      });

      const lines =
        buffer.split("\n");

      buffer = lines.pop() || "";

      for (const line of lines) {
        if (
          !line.startsWith("data:")
        )
          continue;

        try {
          const payload = JSON.parse(
            line.replace("data:", "")
          );

          switch (payload.type) {
            case "token":
              onToken(payload.content);
              break;

            case "tool_start":
              onToolStart?.(
                payload.tool
              );
              break;

            default:
              break;
          }
        } catch (err) {
          console.error(err);
        }
      }
    }
  } catch (error) {
    onError?.(error);
  }
};