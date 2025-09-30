import React, { useState } from "react";
import { View, Text, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { transcribeAudio } from "../utils/api";
import { commonStyles as styles } from "../styles/css";

export default function AudioTranscribe() {
  const navigation = useNavigation<any>();
  const [output, setOutput] = useState("");

  const handleAction = async () => {
    try {
      const res = await transcribeAudio(null); // replace with file input later
      setOutput(res.transcription);
    } catch (error: any) {
      console.error("AudioTranscribe Error:", error);
      setOutput("Error: " + (error.response?.data?.message || error.message));
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Audio Transcribe</Text>

      <TouchableOpacity style={styles.button} onPress={handleAction}>
        <Text style={styles.buttonText}>Run</Text>
      </TouchableOpacity>

      <Text style={styles.output}>Output: {output}</Text>

      <View style={styles.row}>
        {["TextChat", "ImageGen", "Multimodal"].map((screen) => (
          <TouchableOpacity key={screen} style={styles.tabButton} onPress={() => navigation.navigate(screen)}>
            <Text>{screen}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}
