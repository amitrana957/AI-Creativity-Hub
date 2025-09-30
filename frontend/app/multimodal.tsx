import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { multimodalTask } from "../utils/api";
import { commonStyles as styles } from "../styles/css";

export default function Multimodal() {
  const navigation = useNavigation<any>();
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");

  const handleAction = async () => {
    try {
      const res = await multimodalTask({ data: input });
      setOutput(res.result);
    } catch (error: any) {
      console.error("Multimodal Error:", error);
      setOutput("Error: " + (error.response?.data?.message || error.message));
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Multimodal</Text>

      <TextInput style={styles.input} placeholder="Enter input" value={input} onChangeText={setInput} />

      <TouchableOpacity style={styles.button} onPress={handleAction}>
        <Text style={styles.buttonText}>Run</Text>
      </TouchableOpacity>

      <Text style={styles.output}>Output: {output}</Text>

      <View style={styles.row}>
        {["TextChat", "ImageGen", "AudioTranscribe"].map((screen) => (
          <TouchableOpacity key={screen} style={styles.tabButton} onPress={() => navigation.navigate(screen)}>
            <Text>{screen}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}
