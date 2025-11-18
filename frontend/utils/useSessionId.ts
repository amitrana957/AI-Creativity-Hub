import { useState, useEffect } from "react";
import "react-native-get-random-values";
import { v4 as uuidv4 } from "uuid";

export function useSessionId() {
  const [sessionId, setSessionId] = useState("");

  useEffect(() => {
    const newId = uuidv4();
    setSessionId(newId);
  }, []);

  return sessionId;
}
