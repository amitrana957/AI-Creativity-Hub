import React, { useState, useEffect } from "react";
import { View, Text, TextInput, TouchableOpacity, ScrollView, ActivityIndicator, StyleSheet } from "react-native";
import * as DocumentPicker from "expo-document-picker";
import { Audio } from "expo-av";
import Toast from "react-native-toast-message";
import { generateStory, transcribeAudio } from "../utils/api";
import { useSessionId } from "../utils/useSessionId";
import { commonStyles } from "../styles/css";

export default function SpeechScreen() {
  const [topic, setTopic] = useState("");
  const [story, setStory] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [loadingTTS, setLoadingTTS] = useState(false);
  const [loadingSTT, setLoadingSTT] = useState(false);
  const [sound, setSound] = useState<Audio.Sound | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [position, setPosition] = useState(0);
  const [duration, setDuration] = useState(0);
  const [transcript, setTranscript] = useState("");

  const sessionId = useSessionId();

  // ---------- TTS ----------
  const handleGenerateStory = async () => {
    if (!topic.trim()) {
      Toast.show({ type: "info", text1: "Please enter a story topic" });
      return;
    }

    // Reset previous story and audio
    setStory("");
    setAudioUrl("");

    setLoadingTTS(true);
    try {
      const data = await generateStory(topic, sessionId);

      // Use story and audio_url directly from API response
      setStory(data.story);
      setAudioUrl(data.audio_url);

      // Show toast with dynamic message from response
      Toast.show({ type: "success", text1: data.message });
    } catch (err: any) {
      Toast.show({ type: "error", text1: "Failed to generate story", text2: err.message });
    } finally {
      setLoadingTTS(false);
    }
  };

  // ---------- Play / Pause Audio ----------
  const toggleAudio = async () => {
    try {
      if (!audioUrl) return;

      // Create new sound if not exists
      if (!sound) {
        const { sound: newSound } = await Audio.Sound.createAsync({ uri: audioUrl });
        setSound(newSound);
        await newSound.playAsync();
        setIsPlaying(true);

        // Set playback listener
        newSound.setOnPlaybackStatusUpdate((status) => {
          if (status.isLoaded) {
            setPosition(status.positionMillis);
            setDuration(status.durationMillis || 0);
            if (status.didJustFinish) {
              setIsPlaying(false);
              setSound(null);
              setPosition(0);
            }
          }
        });
      } else {
        if (isPlaying) {
          await sound.pauseAsync();
          setIsPlaying(false);
        } else {
          await sound.playAsync();
          setIsPlaying(true);
        }
      }
    } catch (err: any) {
      Toast.show({ type: "error", text1: "Playback Error", text2: err.message });
    }
  };

  const formatTime = (millis: number) => {
    const seconds = Math.floor((millis / 1000) % 60);
    const minutes = Math.floor(millis / 60000);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  };

  // ---------- STT ----------
  const handleUploadAudio = async () => {
    try {
      const result: any = await DocumentPicker.getDocumentAsync({
        type: ["audio/*"],
        copyToCacheDirectory: true,
      });

      if (result.type === "cancel") return;

      const file = result.assets[0];
      if (!file) throw new Error("No file selected");

      setTranscript("");
      setLoadingSTT(true);

      // Fetch blob from URI
      const response = await fetch(file.uri);
      const blob = await response.blob();

      // Convert Blob to File for Web
      const fileForUpload = new File([blob], file.name, {
        type: file.mimeType || "audio/mpeg",
      });

      // Call API helper
      const data = await transcribeAudio(fileForUpload, sessionId);

      setTranscript(data.transcript);
      Toast.show({ type: "success", text1: data.message });
    } catch (err: any) {
      console.error("Upload error:", err);
      Toast.show({
        type: "error",
        text1: "Failed to transcribe audio",
        text2: err.message || "Unknown error",
      });
    } finally {
      setLoadingSTT(false);
    }
  };

  // Cleanup sound on unmount
  useEffect(() => {
    return () => {
      if (sound) {
        sound.unloadAsync();
      }
    };
  }, [sound]);

  return (
    <ScrollView style={commonStyles.screen} contentContainerStyle={commonStyles.scrollContent}>
      {/* ---------- TTS Section ---------- */}
      <View style={commonStyles.card}>
        <Text style={commonStyles.sectionTitle}>🗣️ Text → Speech (TTS)</Text>
        <Text style={commonStyles.sectionDescription}>
          Enter a topic below and generate a story. You can then listen to it as audio.
        </Text>

        <TextInput
          value={topic}
          onChangeText={setTopic}
          placeholder="Enter a story topic..."
          style={commonStyles.input}
        />

        <TouchableOpacity
          onPress={handleGenerateStory}
          disabled={loadingTTS || !topic.trim()}
          style={[
            commonStyles.button,
            { backgroundColor: "#007AFF", flexDirection: "row", justifyContent: "center" },
            (loadingTTS || !topic.trim()) && { opacity: 0.6 },
          ]}
        >
          {loadingTTS && <ActivityIndicator color="#fff" style={{ marginRight: 8 }} />}
          <Text style={commonStyles.buttonText}>{loadingTTS ? "Generating..." : "Generate Story"}</Text>
        </TouchableOpacity>

        {story ? <Text style={commonStyles.outputText}>{story}</Text> : null}

        {audioUrl && (
          <>
            <TouchableOpacity
              onPress={toggleAudio}
              style={[
                commonStyles.button,
                {
                  backgroundColor: "#34C759",
                  marginTop: 15,
                  flexDirection: "row",
                  justifyContent: "center",
                },
              ]}
            >
              <Text style={commonStyles.buttonText}>{isPlaying ? "⏸ Pause Audio" : "▶️ Play Audio"}</Text>
            </TouchableOpacity>

            {/* Audio Progress */}
            <View style={{ marginTop: 10, flexDirection: "row", alignItems: "center" }}>
              <View
                style={{
                  flex: 1,
                  height: 6,
                  backgroundColor: "#eee",
                  borderRadius: 3,
                  overflow: "hidden",
                  marginRight: 8,
                }}
              >
                <View
                  style={{
                    width: duration ? `${(position / duration) * 100}%` : "0%",
                    height: 6,
                    backgroundColor: "#34C759",
                  }}
                />
              </View>
              <Text style={{ fontSize: 12 }}>{formatTime(position)}</Text>
            </View>
          </>
        )}
      </View>

      {/* ---------- STT Section ---------- */}
      <View style={commonStyles.card}>
        <Text style={commonStyles.sectionTitle}>🎤 Speech → Text (STT)</Text>
        <Text style={commonStyles.sectionDescription}>
          Upload an audio file and get the transcription in text format.
        </Text>

        <TouchableOpacity
          onPress={handleUploadAudio}
          disabled={loadingSTT}
          style={[
            commonStyles.button,
            { backgroundColor: "#FF9500", flexDirection: "row", justifyContent: "center" },
            loadingSTT && { opacity: 0.6 },
          ]}
        >
          {loadingSTT && <ActivityIndicator color="#fff" style={{ marginRight: 8 }} />}
          <Text style={commonStyles.buttonText}>
            {loadingSTT ? "Transcribing..." : "Upload Audio for Transcription"}
          </Text>
        </TouchableOpacity>

        {transcript ? <Text style={commonStyles.outputText}>📝 {transcript}</Text> : null}
      </View>
    </ScrollView>
  );
}
