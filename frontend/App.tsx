import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import TextChat from "./app/TextChat";
import ImageGen from "./app/image-gen";
import AudioTranscribe from "./app/audio-transcribe";
import Multimodal from "./app/multimodal";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="TextChat">
        <Stack.Screen name="TextChat" component={TextChat} />
        <Stack.Screen name="ImageGen" component={ImageGen} />
        <Stack.Screen name="AudioTranscribe" component={AudioTranscribe} />
        <Stack.Screen name="Multimodal" component={Multimodal} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
