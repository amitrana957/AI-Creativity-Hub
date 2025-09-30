import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { askText } from "../utils/api";
import { commonStyles } from "../styles/css";
import { validateInput, createSchema } from "../utils/validate";
import { MessageBox } from "../components/MessageBox";
import { Loader } from "../components/Loader"; // <-- import Loader

export default function TextChat() {
  const navigation = useNavigation<any>();
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false); // <-- loader state

  const handleAction = async () => {
    const schema = createSchema("query");
    const { valid, error } = await validateInput(schema, { query: input });

    if (!valid) {
      setErrorMessage(error || "Invalid input");
      setOutput("");
      return;
    }

    setErrorMessage("");
    setLoading(true);

    try {
      const res = await askText(input);
      setOutput(res.answer);
    } catch (error: any) {
      console.error("TextChat Error:", error);
      setOutput("Error: " + (error.response?.data?.message || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={commonStyles.container}>
      <Text style={commonStyles.header}>Text Chat</Text>

      <TextInput style={commonStyles.input} placeholder="Enter text" value={input} onChangeText={setInput} />

      {errorMessage ? <MessageBox type="error" message={errorMessage} /> : null}

      <TouchableOpacity style={commonStyles.button} onPress={handleAction}>
        <Text style={commonStyles.buttonText}>Run</Text>
      </TouchableOpacity>

      {output ? <MessageBox type="success" message={output} /> : null}

      {/* Navigation Buttons */}
      <View style={commonStyles.row}>
        {["ImageGen", "AudioTranscribe", "Multimodal"].map((screen) => (
          <TouchableOpacity key={screen} style={commonStyles.tabButton} onPress={() => navigation.navigate(screen)}>
            <Text>{screen}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Loader */}
      <Loader visible={loading} />
    </View>
  );
}
