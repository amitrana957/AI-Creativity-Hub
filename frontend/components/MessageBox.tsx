import React from "react";
import { View, Text, StyleSheet } from "react-native";

type MessageBoxProps = {
  type: "error" | "success"; // error = red, success = green
  message: string;
};

export const MessageBox: React.FC<MessageBoxProps> = ({ type, message }) => {
  const containerStyle = type === "error" ? styles.errorContainer : styles.successContainer;
  const textStyle = type === "error" ? styles.errorText : styles.successText;

  return (
    <View style={containerStyle}>
      <Text style={textStyle}>
        {type === "error" ? "Error: " : ""}
        {message}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  errorContainer: {
    backgroundColor: "#ff4d4f",
    padding: 10,
    borderRadius: 5,
    marginBottom: 10,
  },
  errorText: {
    color: "#fff",
    fontWeight: "bold",
  },
  successContainer: {
    backgroundColor: "#d9f7be",
    padding: 10,
    borderRadius: 5,
    marginTop: 10,
  },
  successText: {
    color: "#237804",
    fontWeight: "bold",
  },
});
