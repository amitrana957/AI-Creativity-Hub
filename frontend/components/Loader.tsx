// components/Loader.tsx
import React from "react";
import { ActivityIndicator, View, StyleSheet } from "react-native";

export const Loader = ({ visible, size = "small", color = "#fff" }) => {
  if (!visible) return null;

  return (
    <View style={styles.loader}>
      <ActivityIndicator size={size} color={color} />
    </View>
  );
};

const styles = StyleSheet.create({
  loader: {
    marginLeft: 8, // spacing between text and spinner
  },
});
