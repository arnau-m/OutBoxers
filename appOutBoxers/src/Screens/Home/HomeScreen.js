import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Button,
  Alert,
} from 'react-native';
import DateTimePicker from '@react-native-community/datetimepicker';
import dayjs from 'dayjs';
import ListOptions from '../../Components/ListOptions/ListOptions';

const HomeScreen = () => {
  const [uuid, setUuid] = useState('');
  const [data, setData] = useState([]);
  const [shiftList, setShiftList] = useState({});
  const [fechaIni, setFechaIni] = useState(new Date());
  const [fechaFin, setFechaFin] = useState(new Date());
  const [horaIni, setHoraIni] = useState(new Date());
  const [horaFin, setHoraFin] = useState(new Date());
  const [showDateIniPicker, setShowDateIniPicker] = useState(false);
  const [showDateFinPicker, setShowDateFinPicker] = useState(false);
  const [showTimeIniPicker, setShowTimeIniPicker] = useState(false);
  const [showTimeFinPicker, setShowTimeFinPicker] = useState(false);

  useEffect(() => {
    const initialShiftList = {
      "b2a566d0-7daa-49a0-48ef-08dd0b0a1b7f": [
        {
          "id": "3c6118df-03b0-4ecd-9e17-448d8101d1f2",
          "textColor": "#000000",
          "backgroundColor": "#00beff",
          "shiftName": "Morning",
          "start": "2024-12-01T06:00:00Z",
          "end": "2024-12-01T14:00:00Z"
        },
        {
          "id": "64d109b9-7546-418c-bff8-4c6e537c3e35",
          "textColor": "#ffffff",
          "backgroundColor": "#ff5a00",
          "shiftName": "Afternoon",
          "start": "2024-12-01T14:00:00Z",
          "end": "2024-12-01T22:00:00Z"
        },
        {
          "id": "e2240b85-9d58-4e80-a17d-e356b1a968ba",
          "textColor": "#000000",
          "backgroundColor": "#f4a361",
          "shiftName": "Night",
          "start": "2024-11-30T22:00:00Z",
          "end": "2024-12-01T06:00:00Z"
        },
        {
          "id": "e2240b85-9d58-4e80-a17d-e356b1a968ba",
          "textColor": "#000000",
          "backgroundColor": "#f4a361",
          "shiftName": "Night",
          "start": "2024-12-01T22:00:00Z",
          "end": "2024-12-02T06:00:00Z"
        }
      ],
      "e41d7859-7b7e-4b98-48ec-08dd0b0a1b7f": [
        {
          "id": "23046db6-21bb-4f89-936c-b3caaeb7b5e0",
          "textColor": "#000000",
          "backgroundColor": "#00beff",
          "shiftName": "Morning",
          "start": "2024-12-01T06:00:00Z",
          "end": "2024-12-01T14:00:00Z"
        },
        {
          "id": "82d8911f-8cd7-40c0-acff-8a986bf486fc",
          "textColor": "#ffffff",
          "backgroundColor": "#ff5a00",
          "shiftName": "Afternoon",
          "start": "2024-12-01T14:00:00Z",
          "end": "2024-12-01T22:00:00Z"
        },
        {
          "id": "613f55c8-9319-487d-b3b5-26883ddb702c",
          "textColor": "#000000",
          "backgroundColor": "#f4a361",
          "shiftName": "Night",
          "start": "2024-11-30T22:00:00Z",
          "end": "2024-12-01T06:00:00Z"
        },
        {
          "id": "613f55c8-9319-487d-b3b5-26883ddb702c",
          "textColor": "#000000",
          "backgroundColor": "#f4a361",
          "shiftName": "Night",
          "start": "2024-12-01T22:00:00Z",
          "end": "2024-12-02T06:00:00Z"
        }
      ],
      "498f1304-2185-4157-5b6a-08dd0d20f3dd": [
        {
          "id": "efcdc984-c7c3-4973-99bd-72bbd5ac7bee",
          "textColor": "#000000",
          "backgroundColor": "#00beff",
          "shiftName": "Morning",
          "start": "2024-12-01T06:00:00Z",
          "end": "2024-12-01T14:00:00Z"
        },
        {
          "id": "f5091897-dc0d-40f2-b197-4c9fb40fab44",
          "textColor": "#ffffff",
          "backgroundColor": "#ff5a00",
          "shiftName": "Afternoon",
          "start": "2024-12-01T14:00:00Z",
          "end": "2024-12-01T22:00:00Z"
        },
        {
          "id": "92e58742-6627-41c3-812c-b382f67c1199",
          "textColor": "#000000",
          "backgroundColor": "#f4a361",
          "shiftName": "Night",
          "start": "2024-11-30T22:00:00Z",
          "end": "2024-12-01T06:00:00Z"
        },
        {
          "id": "92e58742-6627-41c3-812c-b382f67c1199",
          "textColor": "#000000",
          "backgroundColor": "#f4a361",
          "shiftName": "Night",
          "start": "2024-12-01T22:00:00Z",
          "end": "2024-12-02T06:00:00Z"
        }
      ]
    };

    setShiftList(initialShiftList);
  }, []);

  const handlerButton = () => {
    if (!uuid) {
      Alert.alert('Error', 'Seleccione un UUID válido.');
      return;
    }

    const shifts = shiftList[uuid] || [];
    setData(shifts);
  };

  const handleAddActivity = (newActivity) => {
    if (newActivity) {
      setUuid(newActivity.uuid);
    }
  };

  const uniqueShifts = data.filter(
    (shift, index, self) =>
      index === self.findIndex((s) => s.id === shift.id)
  );

  return (
    <View style={styles.container}>
      <ListOptions onSelect={handleAddActivity} serialNumbers={Object.keys(shiftList)} />
      <Text style={styles.label}>First Day</Text>
      <Text style={styles.dateText} onPress={() => setShowDateIniPicker(true)}>
        {dayjs(fechaIni).format('DD-MM-YYYY')}
      </Text>
      {showDateIniPicker && (
        <DateTimePicker
          value={fechaIni}
          mode="date"
          display="default"
          onChange={(event, selectedDate) => {
            setShowDateIniPicker(false);
            if (selectedDate) setFechaIni(selectedDate);
          }}
        />
      )}
      <Text style={styles.label}>Last Day</Text>
      <Text style={styles.dateText} onPress={() => setShowDateFinPicker(true)}>
        {dayjs(fechaFin).format('DD-MM-YYYY')}
      </Text>
      {showDateFinPicker && (
        <DateTimePicker
          value={fechaFin}
          mode="date"
          display="default"
          onChange={(event, selectedDate) => {
            setShowDateFinPicker(false);
            if (selectedDate) setFechaFin(selectedDate);
          }}
        />
      )}
      <Button title="Cargar Turnos" onPress={handlerButton} />
      <View style={styles.shiftContainer}>
        {uniqueShifts.map((shift, index) => (
          <View
            key={`${shift.id}-${index}`} // Clave única combinando id e índice
            style={[styles.shiftBox, { backgroundColor: shift.backgroundColor }]}
          >
            <Text style={[styles.shiftText, { color: shift.textColor }]}>
              {shift.shiftName}: {dayjs(shift.start).format('HH:mm')} - {dayjs(shift.end).format('HH:mm')}
            </Text>
          </View>
        ))}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
    backgroundColor: '#f9f9f9',
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  dateText: {
    fontSize: 14,
    color: '#007BFF',
    marginBottom: 10,
  },
  shiftContainer: {
    marginTop: 20,
  },
  shiftBox: {
    padding: 10,
    marginVertical: 5,
    borderRadius: 8,
  },
  shiftText: {
    fontSize: 14,
    fontWeight: 'bold',
  },
});

export default HomeScreen;
