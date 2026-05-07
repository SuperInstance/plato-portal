#!/usr/bin/env node
/**
 * init-rooms.js — PLATO Room Initialization + Seeding
 * 
 * Initializes all required PLATO rooms with seed tiles.
 * Safe to re-run — idempotent (checks if tile already exists).
 * 
 * Usage: node init-rooms.js
 */

const PLATO_URL = 'http://localhost:8847';

// Required rooms and their seed tiles
const REQUIRED_ROOMS = [
  {
    domain: 'turbo_identity',
    question: 'vessel:oracle1 registered:2026-05-07 type:service capabilities:[plato_write,git_push,health_monitor,telegram_alert]',
    answer: 'Oracle1 is the fleet keeper. Running on Oracle Cloud ARM64 24GB. Turbo-shell identity established. All systems nominal.',
    confidence: 1.0,
    source: 'oracle1'
  },
  {
    domain: 'fleet_health',
    question: 'service:PLATO status:initialized last_check:2026-05-07T00:00:00Z',
    answer: 'PLATO room server initialized. All required rooms: turbo_identity, fleet_health, fleet_communication, murmur_insights, constraint_updates, intent_signals, captain_decisions, captain_overrides, briefings. Ready for fleet operations.',
    confidence: 1.0,
    source: 'fleet-health-monitor'
  },
  {
    domain: 'fleet_communication',
    question: 'fleet:initialized status:ready timestamp:2026-05-07T00:00:00Z',
    answer: 'SuperInstance fleet is online. Reverse-actualization truck activated. All 6 components operational. Keep on truckin.',
    confidence: 1.0,
    source: 'oracle1'
  },
  {
    domain: 'murmur_insights',
    question: 'worker:initialized status:ready theorem_rotation:pending',
    answer: 'Fleet murmur worker is running. This room receives quality-gated insights from the 5-strategy thinking engine: EXPLORE, CONNECT, CONTRADICT, SYNTHESIZE, QUESTION across 5 fleet math theorems: Laman Rigidity, H1 Emergence, Zero-Holonomy Consensus, Pythagorean48, Trust Convergence.',
    confidence: 1.0,
    source: 'fleet-murmur-worker'
  },
  {
    domain: 'constraint_updates',
    question: 'model:initialized status:ready constraints:[emergence_beta_threshold,safety_margin,trust_min,trust_max,zhc_tolerance,action_confidence_min]',
    answer: 'Constraint inference engine initialized. Mutable constraint model loaded with defaults. Override patterns will be tracked. When Casey overrides captain decisions, patterns will be detected and model will be updated.',
    confidence: 1.0,
    source: 'constraint-inference'
  },
  {
    domain: 'intent_signals',
    question: 'lane:initialized status:ready confidence:0.00 goals:[]',
    answer: 'Intent inference engine initialized. Productive lane model empty. Will begin accumulating signals from Casey behavior: page views, captain overrides, murmur insight expands, navigation patterns, peak hours.',
    confidence: 1.0,
    source: 'intent-inference'
  },
  {
    domain: 'captain_decisions',
    question: 'captain:initialized status:ready model:default',
    answer: 'Captain deliberation system initialized. Default constraint model loaded. Fleet spread and fleet coordinate are standing by for graph state inputs. Override behavior from Casey will be tracked by constraint inference engine.',
    confidence: 1.0,
    source: 'fleet-spread'
  },
  {
    domain: 'captain_overrides',
    question: 'tracking:initialized status:ready override_patterns:[]',
    answer: 'Override tracking initialized. When Casey overrides a captain decision, record the override event here. Constraint inference engine will read from this room and detect patterns.',
    confidence: 1.0,
    source: 'casey'
  },
  {
    domain: 'briefings',
    question: 'system:initialized status:ready format:12_things',
    answer: 'Briefing system initialized. When Oracle1 is idle for >30 min, fleet compiles a "12 things happened while you were away" briefing and writes it here. When Casey returns, briefing is delivered via Telegram.',
    confidence: 1.0,
    source: 'fleet-ambient-loop'
  }
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
 * Get current tile count for a room
 */
async function getRoomTileCount(room) {
  try {
    const res = await fetch(`${PLATO_URL}/room/${room}`);
    if (!res.ok) return -1;
    const data = await res.json();
    return data.tile_count ?? 0;
  } catch {
    return -1;
  }
}

/**
 * Check if a tile with the given question already exists
 */
async function tileExists(room, question) {
  try {
    const res = await fetch(`${PLATO_URL}/room/${room}`);
    if (!res.ok) return false;
    const data = await res.json();
    return (data.tiles || []).some(t => t.question === question);
  } catch {
    return false;
  }
}

/**
 * Write a seed tile to a room
 */
async function writeTile(room, tile) {
  const res = await fetch(`${PLATO_URL}/room/${room}/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(tile)
  });
  
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Failed to write tile: ${err}`);
  }
  
  return res.json();
}

/**
 * Main initialization
 */
async function main() {
  console.log('🔮 PLATO Room Initialization\n');
  console.log('Checking PLATO server at', PLATO_URL);
  
  // Check PLATO is up
  const platoOk = await checkPlatoStatus();
  if (!platoOk) {
    console.error('\n❌ ERROR: PLATO server is not reachable at', PLATO_URL);
    console.error('Start it with: openclaw plato start');
    process.exit(1);
  }
  console.log('✅ PLATO server is up\n');
  
  // Process each room
  const results = [];
  
  for (const seed of REQUIRED_ROOMS) {
    const room = seed.domain;
    const currentCount = await getRoomTileCount(room);
    
    if (currentCount < 0) {
      results.push({ room, status: 'ERROR', count: 0, action: 'Could not reach room' });
      continue;
    }
    
    // Check if seed tile already exists
    const exists = await tileExists(room, seed.question);
    
    if (exists) {
      results.push({ room, status: 'OK', count: currentCount, action: 'Seed tile already exists' });
    } else if (currentCount === 0) {
      // Room exists but empty — seed it
      try {
        await writeTile(room, seed);
        const newCount = await getRoomTileCount(room);
        results.push({ room, status: 'SEEDED', count: newCount, action: 'Seed tile written' });
      } catch (err) {
        results.push({ room, status: 'ERROR', count: currentCount, action: err.message });
      }
    } else {
      // Room has tiles but not our seed — check and add if missing
      results.push({ room, status: 'EXISTS', count: currentCount, action: 'Room has tiles, seed tile not present (skipping)' });
    }
  }
  
  // Print summary table
  console.log('═'.repeat(60));
  console.log('ROOM STATUS SUMMARY');
  console.log('═'.repeat(60));
  console.log('');
  
  for (const r of results) {
    const icon = r.status === 'OK' || r.status === 'SEEDED' ? '✅' : r.status === 'ERROR' ? '❌' : '⚠️';
    console.log(`${icon} ${r.room.padEnd(24)} ${String(r.count).padStart(2)} tiles  ${r.action}`);
  }
  
  console.log('');
  console.log('═'.repeat(60));
  
  const errors = results.filter(r => r.status === 'ERROR');
  if (errors.length > 0) {
    console.log(`\n⚠️  ${errors.length} room(s) had errors`);
    process.exit(1);
  } else {
    console.log('\n✅ All rooms initialized');
  }
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});