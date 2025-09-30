import React from "react";
import { View, ActivityIndicator, StyleSheet } from "react-native";

type LoaderProps = {
  visible: boolean;
};

export const Loader: React.FC<LoaderProps> = ({ visible }) => {
  if (!visible) return null;

  return (
    <View style={styles.overlay}>
      <ActivityIndicator size="large" color="#1890ff" />
    </View>
  );
};

const styles = StyleSheet.create({
  overlay: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(0,0,0,0.25)",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 999,
  },
});
