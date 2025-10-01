import { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid"; // npm i uuid

export function useSessionId() {
  const [sessionId, setSessionId] = useState("");

  useEffect(() => {
    const newId = uuidv4();
    setSessionId(newId); // generate unique session per refresh
  }, []);

  return sessionId;
}
