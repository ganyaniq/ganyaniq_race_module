import React, { useState, useEffect } from 'react';
import { Text, View, StyleSheet, ScrollView, RefreshControl, Pressable } from 'react-native';

const API_BASE = 'https://29979c87-7fb3-41d1-b125-3c81a754a64f.preview.emergentagent.com';
const today = new Date().toISOString().split('T')[0];

export default function Index() {
  const [races, setRaces] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [results, setResults] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = async () => {
    try {
      const [programRes, predRes, resultsRes] = await Promise.all([
        fetch(`${API_BASE}/api/program-lite?day=${today}`),
        fetch(`${API_BASE}/api/predictions?day=${today}`),
        fetch(`${API_BASE}/api/results-lite?day=${today}`)
      ]);
      
      const programData = await programRes.json();
      const predData = await predRes.json();
      const resultsData = await resultsRes.json();
      
      setRaces(programData.rows || []);
      setPredictions(predData.predictions || []);
      setResults(resultsData.rows || []);
    } catch (err) {
      console.error('Data load error:', err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      <View style={styles.header}>
        <Text style={styles.title}>🏇 GANYAN IQ</Text>
        <Text style={styles.subtitle}>At Yarışları AI Tahmin Platformu</Text>
      </View>

      <View style={styles.stats}>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{races.length}</Text>
          <Text style={styles.statLabel}>Günlük Yarış</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={[styles.statNumber, {color: '#3b82f6'}]}>{predictions.length}</Text>
          <Text style={styles.statLabel}>AI Tahmini</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📋 Yarış Programı</Text>
        {races.slice(0, 5).map((race, i) => (
          <View key={i} style={styles.raceCard}>
            <View style={styles.raceHeader}>
              <Text style={styles.raceHippo}>{race.hippodrome}</Text>
              <Text style={styles.raceNo}>Koşu {race.race_no}</Text>
            </View>
            <View style={styles.raceDetails}>
              <Text style={styles.raceDetail}>{race.distance} • {race.type}</Text>
              <Text style={styles.raceTime}>{race.start_time}</Text>
            </View>
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>🤖 Alfonso AI Tahminleri</Text>
        {predictions.slice(0, 2).map((pred, i) => (
          <View key={i} style={styles.predCard}>
            <View style={styles.predHeader}>
              <Text style={styles.predTitle}>{pred.race_info?.hippodrome} - Koşu {pred.race_info?.race_no}</Text>
              <View style={styles.badge}>
                <Text style={styles.badgeText}>{pred.confidence_level}</Text>
              </View>
            </View>
            {pred.predictions?.slice(0, 3).map((p, j) => (
              <View key={j} style={styles.predItem}>
                <View style={styles.horseNumber}>
                  <Text style={styles.horseNumberText}>{p.horse_number}</Text>
                </View>
                <View style={styles.predInfo}>
                  <Text style={styles.predRank}>{j === 0 ? '🥇' : j === 1 ? '🥈' : '🥉'} {j + 1}. Tercih</Text>
                  <Text style={styles.predReason}>{p.reason}</Text>
                  <Text style={styles.predConfidence}>Güven: %{p.confidence}</Text>
                </View>
              </View>
            ))}
            <View style={styles.analysis}>
              <Text style={styles.analysisText}>{pred.analysis}</Text>
            </View>
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>🏆 Sonuçlar</Text>
        {results.map((result, i) => (
          <View key={i} style={styles.resultCard}>
            <View style={styles.resultHeader}>
              <Text style={styles.resultHippo}>{result.hippodrome}</Text>
              <Text style={styles.resultNo}>Koşu {result.race_no}</Text>
            </View>
            <View style={styles.resultDetails}>
              <Text style={styles.resultText}>1. {result.first} • 2. {result.second}</Text>
              <Text style={styles.ganyan}>Ganyan: {result.ganyan} TL</Text>
            </View>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0b0f14',
  },
  header: {
    paddingTop: 60,
    paddingBottom: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#fbbf24',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#9ca3af',
  },
  stats: {
    flexDirection: 'row',
    padding: 16,
    gap: 16,
  },
  statCard: {
    flex: 1,
    backgroundColor: 'rgba(18,24,34,0.7)',
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#10b981',
  },
  statLabel: {
    fontSize: 14,
    color: '#9ca3af',
    marginTop: 8,
  },
  section: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fbbf24',
    marginBottom: 16,
  },
  raceCard: {
    backgroundColor: 'rgba(31,41,55,0.5)',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: 'rgba(75,85,99,0.5)',
  },
  raceHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  raceHippo: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fbbf24',
  },
  raceNo: {
    fontSize: 14,
    color: '#d1d5db',
  },
  raceDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  raceDetail: {
    fontSize: 12,
    color: '#9ca3af',
  },
  raceTime: {
    fontSize: 12,
    color: '#10b981',
    fontWeight: '600',
  },
  predCard: {
    backgroundColor: 'rgba(18,24,34,0.7)',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  predHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  predTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fbbf24',
  },
  badge: {
    backgroundColor: 'rgba(16,185,129,0.2)',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  badgeText: {
    fontSize: 12,
    color: '#10b981',
  },
  predItem: {
    flexDirection: 'row',
    backgroundColor: 'rgba(31,41,55,0.6)',
    borderRadius: 12,
    padding: 12,
    marginBottom: 12,
  },
  horseNumber: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#fbbf24',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  horseNumberText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#0b0f14',
  },
  predInfo: {
    flex: 1,
  },
  predRank: {
    fontSize: 14,
    fontWeight: '600',
    color: '#e8eefb',
    marginBottom: 4,
  },
  predReason: {
    fontSize: 12,
    color: '#9ca3af',
    marginBottom: 4,
  },
  predConfidence: {
    fontSize: 12,
    color: '#10b981',
    fontWeight: '600',
  },
  analysis: {
    backgroundColor: 'rgba(59,130,246,0.1)',
    borderRadius: 8,
    padding: 12,
    marginTop: 8,
    borderWidth: 1,
    borderColor: 'rgba(59,130,246,0.3)',
  },
  analysisText: {
    fontSize: 12,
    color: '#d1d5db',
    lineHeight: 18,
  },
  resultCard: {
    backgroundColor: 'rgba(31,41,55,0.5)',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: 'rgba(75,85,99,0.5)',
  },
  resultHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  resultHippo: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fbbf24',
  },
  resultNo: {
    fontSize: 14,
    color: '#d1d5db',
  },
  resultDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  resultText: {
    fontSize: 12,
    color: '#9ca3af',
  },
  ganyan: {
    fontSize: 12,
    color: '#10b981',
    fontWeight: '600',
  },
});