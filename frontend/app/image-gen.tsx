import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { generateImage } from "../utils/api";
import { commonStyles as styles } from "../styles/css";

export default function ImageGen() {
  const navigation = useNavigation<any>();
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");

  const handleAction = async () => {
    try {
      const res = await generateImage(input);
      setOutput(res.image_url);
    } catch (error: any) {
      console.error("ImageGen Error:", error);
      setOutput("Error: " + (error.response?.data?.message || error.message));
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Image Generator</Text>

      <TextInput style={styles.input} placeholder="Enter prompt" value={input} onChangeText={setInput} />

      <TouchableOpacity style={styles.button} onPress={handleAction}>
        <Text style={styles.buttonText}>Run</Text>
      </TouchableOpacity>

      <Text style={styles.output}>Output URL: {output}</Text>

      <View style={styles.row}>
        {["TextChat", "AudioTranscribe", "Multimodal"].map((screen) => (
          <TouchableOpacity key={screen} style={styles.tabButton} onPress={() => navigation.navigate(screen)}>
            <Text>{screen}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}
