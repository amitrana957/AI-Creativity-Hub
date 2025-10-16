import { StyleSheet } from "react-native";

export const commonStyles = StyleSheet.create({
  // ---------- Existing styles ----------
  container: {
    flex: 1,
    backgroundColor: "#f5f5f7",
    paddingTop: 40,
    paddingHorizontal: 10,
  },
  header: { fontSize: 24, fontWeight: "700", textAlign: "center", color: "#111827", marginBottom: 10 },
  chatContainer: { flexGrow: 1, justifyContent: "flex-end", paddingBottom: 10 },
  messageBubble: { marginVertical: 5, padding: 12, borderRadius: 16, maxWidth: "80%" },
  userBubble: { alignSelf: "flex-end", backgroundColor: "#DCF8C6" },
  assistantBubble: { alignSelf: "flex-start", backgroundColor: "#E5E5EA" },
  messageText: { fontSize: 16, lineHeight: 22, color: "#111827" },
  inputRow: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    paddingHorizontal: 5,
    borderTopWidth: 1,
    borderColor: "#ccc",
    backgroundColor: "#fff",
  },
  chatInput: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 25,
    paddingHorizontal: 15,
    paddingVertical: 8,
    fontSize: 16,
    marginRight: 10,
  },
  sendButton: { paddingHorizontal: 15, paddingVertical: 10, backgroundColor: "#007AFF", borderRadius: 25 },
  sendText: { color: "#fff", fontWeight: "bold" },
  typingText: { fontStyle: "italic", color: "#666", marginVertical: 5, marginLeft: 10 },
  row: { flexDirection: "row", justifyContent: "space-between", marginTop: 5, marginBottom: 10 },
  tabButton: {
    backgroundColor: "#e5e7eb",
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 8,
    minWidth: 100,
    alignItems: "center",
  },
  tabButtonText: { fontWeight: "500", color: "#111827" },

  // ---------- New SpeechScreen styles ----------
  screen: {
    flex: 1,
    backgroundColor: "#f2f2f7",
    padding: 15,
  },
  scrollContent: {
    paddingBottom: 30,
  },
  card: {
    backgroundColor: "#fff",
    padding: 20,
    borderRadius: 15,
    marginBottom: 20,
    // iOS shadow
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 3 },
    // Android elevation
    elevation: 4,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: "700",
    marginBottom: 10,
  },
  sectionDescription: {
    fontSize: 14,
    color: "#555",
    marginBottom: 10,
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 12,
    borderRadius: 10,
    marginBottom: 15,
    backgroundColor: "#f9f9f9",
  },
  button: {
    padding: 12,
    borderRadius: 10,
    alignItems: "center",
  },
  buttonText: {
    color: "#fff",
    fontWeight: "600",
  },
  outputText: {
    marginTop: 15,
    fontSize: 16,
  },
});
