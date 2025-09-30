// frontend/app/styles.ts
import { StyleSheet } from "react-native";

export const commonStyles = StyleSheet.create({
  // Main container for all screens
  container: {
    flex: 1,
    backgroundColor: "#f9fafb", // lighter gray background
    padding: 20,
  },

  // Screen headers
  header: {
    fontSize: 28,
    fontWeight: "700",
    color: "#111827", // dark gray
    marginBottom: 20,
  },

  // Smaller bold text (like subtitles)
  boldText: {
    fontWeight: "700",
    fontSize: 18,
    color: "#1f2937",
    marginBottom: 10,
  },

  // Text inputs
  input: {
    borderWidth: 1,
    borderColor: "#d1d5db", // gray border
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 10,
    marginBottom: 20,
    backgroundColor: "#ffffff",
    fontSize: 16,
    color: "#111827",
  },

  // Buttons
  button: {
    backgroundColor: "#3b82f6", // blue-500
    paddingVertical: 14,
    borderRadius: 10,
    marginBottom: 20,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 3, // adds Android shadow
  },

  buttonText: {
    color: "#ffffff",
    textAlign: "center",
    fontWeight: "600",
    fontSize: 16,
  },

  // Output text
  output: {
    color: "#374151", // gray-700
    fontSize: 16,
    marginBottom: 20,
    lineHeight: 22,
  },

  // Row for navigation buttons
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 10,
  },

  tabButton: {
    backgroundColor: "#e5e7eb", // gray-200
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 8,
    minWidth: 100,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },

  tabButtonText: {
    fontWeight: "500",
    color: "#111827",
  },
});
