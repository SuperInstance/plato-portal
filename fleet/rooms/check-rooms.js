#!/usr/bin/env node
/**
 * check-rooms.js — PLATO Room Status Checker
 * 
 * Reports current state of all required rooms without writing.
 * 
 * Usage: node check-rooms.js
 */

const PLATO_URL = 'http://localhost:8847';

const REQUIRED_ROOMS = [
  'turbo_identity',
  'fleet_health',
  'fleet_communication',
  'murmur_insights',
  'constraint_updates',
  'intent_signals',
  'captain_decisions',
  'captain_overrides',
  'briefings'
];

/**
 * Check if PLATO server is reachable
 */
async function checkPlatoStatus() {
  try {
    const res = await fetch(`${PLATO_URL}/rooms`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return true;
  } catch (err) {
    return false;
  }
}

/**
 * Get room info
 */
async function getRoomInfo(room) {
  try {
    const res = await fetch(`${PLATO_URL}/room/${room}`);
    if (!res.ok) return { tile_count: -1, error: `HTTP ${res.status}` };
    const data = await res.json();
    return { tile_count: data.tile_count ?? 0, error: null };
  } catch (err) {
    return { tile_count: -1, error: err.message };
  }
}

/**
 * Get status label
 */
function getStatusLabel(count, room) {
  if (count < 0) return 'ERROR';
  if (count === 0) {
    if (room === 'captain_overrides') return 'empty — waiting for overrides';
    if (room === 'briefings') return 'empty — no briefings yet';
    return 'empty';
  }
  return 'ok';
}

/**
 * Main
 */
async function main() {
  console.log('=== PLATO Room Status ===\n');
  
  // Check PLATO is up
  const platoOk = await checkPlatoStatus();
  if (!platoOk) {
    console.error('ERROR: PLATO server is not reachable at', PLATO_URL);
    console.error('Start it with: openclaw plato start');
    process.exit(1);
  }
  
  // Check each room
  const results = await Promise.all(
    REQUIRED_ROOMS.map(async (room) => {
      const info = await getRoomInfo(room);
      return { room, ...info };
    })
  );
  
  // Print results
  for (const r of results) {
    const label = getStatusLabel(r.tile_count, r.room);
    const countStr = r.tile_count < 0 ? '--' : String(r.tile_count);
    const status = r.tile_count < 0 ? '❌' : r.tile_count === 0 ? '○' : '✓';
    console.log(`${status} ${r.room.padEnd(20)} ${countStr.padStart(2)} tiles (${label})`);
  }
  
  console.log('\nPLATO server: ' + PLATO_URL);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});