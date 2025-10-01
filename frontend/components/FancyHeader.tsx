import React from "react";
import { Text, View, StyleSheet } from "react-native";

export function FancyHeader() {
  return (
    <View style={styles.headerContainer}>
      <Text style={styles.headerText}>🤖 Langchain ChatAI</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  headerContainer: {
    marginVertical: 20,
    alignItems: "center",
  },
  headerText: {
    fontSize: 32,
    fontWeight: "900",
    textAlign: "center",
    color: "#4c669f", // base color
  },
});
