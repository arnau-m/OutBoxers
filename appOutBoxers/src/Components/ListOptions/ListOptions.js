import React, { useState } from 'react'; 
import { View, TextInput, Text, TouchableOpacity, FlatList, StyleSheet, Alert } from 'react-native';

const hardcodedData = [
  { uuid: "e41d7859-7b7e-4b98-48ec-08dd0b0a1b7f", serialNumber: "lauzhack-pi1" },
  { uuid: "498f1304-2185-4157-5b6a-08dd0d20f3dd", serialNumber: "lauzhack-pi10" },
  { uuid: "bd547715-e272-4b80-5b6b-08dd0d20f3dd", serialNumber: "lauzhack-pi11" },
  { uuid: "0494fc4a-eedb-4828-5b72-08dd0d20f3dd", serialNumber: "lauzhack-pi12" },
  { uuid: "7897794a-a29b-4544-48ed-08dd0b0a1b7f", serialNumber: "lauzhack-pi2" },
  { uuid: "e646e70b-8af2-4165-48ee-08dd0b0a1b7f", serialNumber: "lauzhack-pi3" },
  { uuid: "b2a566d0-7daa-49a0-48ef-08dd0b0a1b7f", serialNumber: "lauzhack-pi4" },
  { uuid: "87d24a68-8fde-4cb6-48f0-08dd0b0a1b7f", serialNumber: "lauzhack-pi5" },
  { uuid: "8e779337-7ef8-4bf5-5b67-08dd0d20f3dd", serialNumber: "lauzhack-pi6" },
  { uuid: "ef948b22-553d-4257-4eac-08dd0cfb4535", serialNumber: "lauzhack-pi7" },
  { uuid: "c86546e5-27c8-4899-5b68-08dd0d20f3dd", serialNumber: "lauzhack-pi8" },
  { uuid: "e5639a1d-36e2-4d29-5b69-08dd0d20f3dd", serialNumber: "lauzhack-pi9" },
];

const ListOptions = ({ onSelect }) => {
  const [query, setQuery] = useState('');
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [activitiesList] = useState(hardcodedData); // Lista inicializada con los datos hardcodeados
  const [showDropdown, setShowDropdown] = useState(false);

  const handleInputChange = (text) => {
    setQuery(text);

    if (text.length >= 1) {
      const matches = activitiesList.filter(activity =>
        activity.serialNumber.toLowerCase().includes(text.toLowerCase())
      );

      setFilteredUsers(matches.length !== 0 ? matches : []);
      setShowDropdown(matches.length !== 0);
    } else {
      setFilteredUsers([]);
      setShowDropdown(false);
    }
  };

  const handleSelect = (activity) => {
    const exists = activitiesList.some(item => item === activity);

    if (exists) {
        setQuery(activity.serialNumber)
      onSelect(activity);
    } else {
      Alert.alert(
        'SerialNumber no encontrada',
        `La SerialNumber "${activity}" no existe en la lista.`,
        [{ text: 'OK' }]
      );
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Type a SerialNumber name"
        value={query}
        onChangeText={handleInputChange}
      />
      {showDropdown && (
        <FlatList
          data={filteredUsers}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item }) => (
            <TouchableOpacity onPress={() => handleSelect(item)}>
              <Text style={styles.dropdownItem}>{item.serialNumber}</Text>
            </TouchableOpacity>
          )}
          style={styles.dropdown}
          keyboardShouldPersistTaps="handled"
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    marginVertical: 10,
  },
  input: {
    padding: 10,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    fontSize: 16,
  },
  dropdown: {
    backgroundColor: '#fff',
    borderColor: '#ccc',
    borderWidth: 1,
    borderTopWidth: 0,
    borderRadius: 5,
    maxHeight: 150,
    marginTop: 2,
  },
  dropdownItem: {
    padding: 10,
    borderBottomColor: '#eee',
    borderBottomWidth: 1,
    fontSize: 16,
  },
});

export default ListOptions;
