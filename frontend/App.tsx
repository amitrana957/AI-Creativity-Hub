// App.tsx
import React from "react";
import { TouchableOpacity, View, Text, Modal } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import TextChat from "./app/TextChat";
import SpeechScreen from "./app/SpeechScreen";
import { Ionicons } from "@expo/vector-icons";
import Toast from "react-native-toast-message"; // ✅ import Toast

const Stack = createNativeStackNavigator();

function HeaderMenu({ navigation }: any) {
  const [visible, setVisible] = React.useState(false);

  const screens = [
    { name: "TextChat", label: "💬 Text Chat" },
    { name: "SpeechScreen", label: "🗣️ Speech AI" },
  ];

  return (
    <View>
      <TouchableOpacity onPress={() => setVisible(true)} style={{ padding: 5 }}>
        <Ionicons name="menu" size={24} color="#007AFF" />
      </TouchableOpacity>

      <Modal visible={visible} transparent animationType="fade" onRequestClose={() => setVisible(false)}>
        <TouchableOpacity
          style={{
            flex: 1,
            backgroundColor: "rgba(0,0,0,0.3)",
            justifyContent: "flex-start",
            alignItems: "flex-end",
          }}
          activeOpacity={1}
          onPressOut={() => setVisible(false)}
        >
          <View
            style={{
              backgroundColor: "#fff",
              borderRadius: 10,
              marginTop: 60,
              marginRight: 10,
              paddingVertical: 5,
              width: 180,
              shadowColor: "#000",
              shadowOpacity: 0.2,
              shadowRadius: 4,
              elevation: 3,
            }}
          >
            {screens.map((item) => (
              <TouchableOpacity
                key={item.name}
                style={{
                  padding: 10,
                  borderBottomWidth: 0.5,
                  borderBottomColor: "#eee",
                }}
                onPress={() => {
                  navigation.navigate(item.name);
                  setVisible(false);
                }}
              >
                <Text style={{ fontSize: 16 }}>{item.label}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </TouchableOpacity>
      </Modal>
    </View>
  );
}

export default function App() {
  return (
    <>
      <NavigationContainer>
        <Stack.Navigator
          initialRouteName="SpeechScreen"
          screenOptions={({ navigation }) => ({
            headerRight: () => <HeaderMenu navigation={navigation} />,
            headerTitleAlign: "center",
          })}
        >
          <Stack.Screen name="TextChat" component={TextChat} options={{ title: "💬 Chat AI" }} />
          <Stack.Screen name="SpeechScreen" component={SpeechScreen} options={{ title: "🗣️ Speech AI" }} />
        </Stack.Navigator>
      </NavigationContainer>

      {/* ✅ Toast MUST be here, outside the navigator */}
      <Toast />
    </>
  );
}
