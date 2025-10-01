import React, { useState, useEffect, useRef } from "react";
import { View, Text, TextInput, TouchableOpacity, FlatList, KeyboardAvoidingView, Platform } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { commonStyles } from "../styles/css";
import { Loader } from "../components/Loader";
import { askText } from "../utils/api";
import { useSessionId } from "../utils/useSessionId";

export default function TextChat() {
  const navigation = useNavigation<any>();
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const sessionId = useSessionId();

  const flatListRef = useRef<FlatList>(null);

  // ---------------- Auto-scroll whenever messages change ----------------
  useEffect(() => {
    if (flatListRef.current && messages.length > 0) {
      flatListRef.current.scrollToEnd({ animated: true });
    }
  }, [messages]);

  // ---------------- Send message ----------------
  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await askText(userMessage, sessionId); // pass session ID
      setMessages((prev) => [...prev, res.answer || res]); // res can be string or { answer }
    } catch (error: any) {
      setMessages((prev) => [...prev, "Error: " + (error.message || "Unknown")]);
    } finally {
      setLoading(false);
    }
  };

  // ---------------- Render each message ----------------
  const renderMessage = ({ item, index }: { item: string; index: number }) => {
    const isUser = index % 2 === 0;
    return (
      <View style={[commonStyles.messageBubble, isUser ? commonStyles.userBubble : commonStyles.assistantBubble]}>
        <Text style={commonStyles.messageText}>{item}</Text>
      </View>
    );
  };

  return (
    <KeyboardAvoidingView
      style={commonStyles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
      keyboardVerticalOffset={Platform.OS === "ios" ? 90 : 0}
    >
      {/* Header */}
      <Text style={commonStyles.header}>🤖 ChatAI</Text>

      {/* Messages */}
      <FlatList
        ref={flatListRef}
        data={messages}
        keyExtractor={(_, index) => index.toString()}
        renderItem={renderMessage}
        contentContainerStyle={{ padding: 10, flexGrow: 1 }}
        keyboardShouldPersistTaps="handled"
      />

      {/* Typing indicator */}
      {loading && <Text style={commonStyles.typingText}>Assistant is typing...</Text>}

      {/* Input */}
      <View style={commonStyles.inputRow}>
        <TextInput
          style={commonStyles.chatInput}
          placeholder="Type a message..."
          value={input}
          onChangeText={setInput}
          editable={!loading}
          returnKeyType="send"
          onSubmitEditing={() => {
            if (input.trim().length > 0) handleSend();
          }}
        />
        <TouchableOpacity
          style={[commonStyles.sendButton, { opacity: input.trim().length === 0 || loading ? 0.5 : 1 }]}
          onPress={handleSend}
          disabled={input.trim().length === 0 || loading}
        >
          {loading ? <Loader visible={true} /> : <Text style={commonStyles.sendText}>Send</Text>}
        </TouchableOpacity>
      </View>

      {/* Tabs */}
      <View style={commonStyles.row}>
        {["ImageGen", "AudioTranscribe", "Multimodal"].map((screen) => (
          <TouchableOpacity key={screen} style={commonStyles.tabButton} onPress={() => navigation.navigate(screen)}>
            <Text style={commonStyles.tabButtonText}>{screen}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </KeyboardAvoidingView>
  );
}
