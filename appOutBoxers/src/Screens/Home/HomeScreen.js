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
import api from '../../Utils/api';

const HomeScreen = () => {
  const [uuid, setUuid] = useState('');
  const [shiftList, setShiftList] = useState([]);
  const [fechaIni, setFechaIni] = useState(new Date());
  const [fechaFin, setFechaFin] = useState(new Date());
  const [showDateIniPicker, setShowDateIniPicker] = useState(false);
  const [showDateFinPicker, setShowDateFinPicker] = useState(false);

  useEffect(() => {
    if (!uuid) {
      Alert.alert('Error', 'UUID no está definido.');
      return;
    }
  }, [uuid]);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const objParams = { serialNumber: 'lauzhack-pi4' };
        const response = await api.get('remoteassistance/v1/equipments', objParams);
        setUuid(response[0]?.uuid);
      } catch (error) {
        console.error('Error obteniendo el UUID:', error);
        Alert.alert('Error', 'No se pudo obtener el UUID.');
      }
    };

    fetchInitialData();
  }, []);

  const handlerButton = async () => {
    try {
      const startTimestamp = fechaIni.toISOString();
      const endTimestamp = fechaFin.toISOString();
      const endpoint = `performance/v1/${uuid}/shift?startTimestamp=${encodeURIComponent(
        startTimestamp
      )}&endTimestamp=${encodeURIComponent(endTimestamp)}`;
      const response = await api.get(endpoint);
      setShiftList(response);
    } catch (error) {
      console.error('Error al obtener los turnos:', error);
      Alert.alert('Error', 'No se pudieron cargar los turnos.');
    }
  };

  // Filtrar turnos duplicados por ID
  const uniqueShifts = shiftList.filter(
    (shift, index, self) =>
      index === self.findIndex(s => s.id === shift.id) // Mantiene solo el primer elemento con un ID único
  );

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.label}>UUID: {uuid || 'No definido'}</Text>
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
    </ScrollView>
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
