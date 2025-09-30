import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { askText } from "../utils/api";
import { commonStyles } from "../styles/css";

export default function TextChat() {
  const navigation = useNavigation<any>();
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");

  const handleAction = async () => {
    try {
      const res = await askText(input);
      setOutput(res.answer);
    } catch (error: any) {
      console.error("TextChat Error:", error);
      setOutput("Error: " + (error.response?.data?.message || error.message));
    }
  };

  return (
    <View style={commonStyles.container}>
      <Text style={commonStyles.header}>Text Chat</Text>

      <TextInput style={commonStyles.input} placeholder="Enter text" value={input} onChangeText={setInput} />

      <TouchableOpacity style={commonStyles.button} onPress={handleAction}>
        <Text style={commonStyles.buttonText}>Run</Text>
      </TouchableOpacity>

      <Text style={commonStyles.output}>Output: {output}</Text>

      <View style={commonStyles.row}>
        {["ImageGen", "AudioTranscribe", "Multimodal"].map((screen) => (
          <TouchableOpacity key={screen} style={commonStyles.tabButton} onPress={() => navigation.navigate(screen)}>
            <Text>{screen}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}
