import { Box } from "@mui/material";
import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";

export default function MessageList({ messages = [], onSuggestedReply }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  return (
    <Box
      sx={{
        flex: 1,
        overflowY: "auto",
        p: 2,
        display: "flex",
        flexDirection: "column",
        gap: 2,
      }}
    >
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          message={message}
          onSuggestedReply={onSuggestedReply}
        />
      ))}

      <div ref={bottomRef} />
    </Box>
  );
}
