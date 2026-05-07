/**
 * Quality Score Schema
 * Tile quality labels and overall quality scoring
 */

export interface TileQualityLabel {
  novelty: number;    // 0-1: How novel/original is this tile
  correctness: number; // 0-1: How correct/valid is this tile
  completeness: number; // 0-1: How complete is this tile
  depth: number;     // 0-1: How deep/sophisticated is this tile
  overall: number;   // 0-1: Weighted composite score
}

export interface QualityScore {
  tile_id: string;
  version: number;
  labels: TileQualityLabel;
  assessed_at: number;
  assessor?: string;
  reasoning?: string;
  metadata?: Record<string, unknown>;
}
