#!/usr/bin/env python3
"""
Generate forecast data for margin debt regime dashboard.

This script:
1. Loads regime_history.csv
2. Classifies data into states (E_up, G_flat, etc.)
3. Generates transition probabilities
4. Creates forecast_data.json with predictions for each month
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

# Thresholds
TH = 30.0  # Regime threshold (percentage)
M_TH = 2.0  # Momentum threshold (pp/month)
MA = 3     # Moving average window

# ============================================================================
# DATA PREPARATION
# ============================================================================

def load_and_classify_data(csv_path):
    """Load CSV and add state classifications."""
    df = pd.read_csv(csv_path)
    
    # Rename columns for consistency
    df = df.rename(columns={
        'Date': 'date',
        'YoY_Change_%': 'yoy_pct'
    })
    
    # Parse dates
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    # Smooth YoY to reduce noise
    df['yoy_ma'] = df['yoy_pct'].rolling(MA, min_periods=1).mean()
    
    # Calculate rate of change (momentum)
    df['dyoy'] = df['yoy_ma'].diff()
    
    # Classify base regime
    def base_regime(y):
        if pd.isna(y): return np.nan
        if y >= TH: return "E"
        if y >= 0: return "G"
        if y > -TH: return "C"
        return "D"
    
    # Classify momentum
    def momentum(d):
        if pd.isna(d): return np.nan
        if d >= M_TH: return "up"
        if d <= -M_TH: return "down"
        return "flat"
    
    df['regime'] = df['yoy_ma'].apply(base_regime)
    df['mom'] = df['dyoy'].apply(momentum)
    
    # Combine into state
    df['state'] = df['regime'] + '_' + df['mom']
    df.loc[df['regime'].isna() | df['mom'].isna(), 'state'] = np.nan
    
    return df

# ============================================================================
# TRANSITION PROBABILITY ESTIMATION
# ============================================================================

def estimate_transitions(df):
    """
    Estimate P(state_{t+1} | state_t) using expanding window.
    Returns dict mapping each date to its transition probabilities.
    """
    forecasts = []
    
    for i in range(len(df)):
        row = df.iloc[i]
        current_date = row['date']
        current_state = row['state']
        
        if pd.isna(current_state):
            continue
        
        # Use only data BEFORE this date (expanding window)
        hist = df[df.index < i].copy()
        
        # Need at least 12 months of history
        if len(hist) < 12:
            continue
        
        # Get next states for historical data
        hist['next_state'] = hist['state'].shift(-1)
        hist = hist.dropna(subset=['state', 'next_state'])
        
        # Calculate transition probabilities from current_state
        transitions = hist[hist['state'] == current_state]['next_state']
        
        if len(transitions) == 0:
            # No historical data for this state
            continue
        
        # Calculate probabilities
        probs = transitions.value_counts(normalize=True)
        
        # Get top 5 predictions
        top5 = probs.nlargest(5)
        
        # Aggregate by regime
        regime_probs = {}
        for state, prob in probs.items():
            regime = state[0]
            regime_probs[regime] = regime_probs.get(regime, 0) + prob
        
        # Build forecast entry
        forecast = {
            'date': current_date.strftime('%Y-%m-%d'),
            'pred_state': probs.idxmax(),
            'confidence': float(probs.max()),
            'prob_E': float(regime_probs.get('E', 0)),
            'prob_G': float(regime_probs.get('G', 0)),
            'prob_C': float(regime_probs.get('C', 0)),
            'prob_D': float(regime_probs.get('D', 0))
        }
        
        # Add top 5 predictions
        for idx, (state, prob) in enumerate(top5.items(), 1):
            forecast[f'top{idx}_state'] = state
            forecast[f'top{idx}_prob'] = float(prob)
        
        # Fill remaining slots with None
        for idx in range(len(top5) + 1, 6):
            forecast[f'top{idx}_state'] = None
            forecast[f'top{idx}_prob'] = 0.0
        
        forecasts.append(forecast)
    
    return forecasts

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*80)
    print("MARGIN DEBT FORECAST GENERATOR")
    print("="*80)
    
    # Load data
    print("\n[1/3] Loading and classifying data...")
    df = load_and_classify_data('regime_history.csv')
    print(f"  Loaded {len(df)} months of data")
    print(f"  Date range: {df['date'].min().strftime('%Y-%m')} to {df['date'].max().strftime('%Y-%m')}")
    
    # Show state distribution
    state_counts = df['state'].value_counts()
    print(f"\n  Found {len(state_counts)} unique states:")
    for state, count in state_counts.head(10).items():
        print(f"    {state}: {count} months")
    
    # Generate forecasts
    print("\n[2/3] Generating forecasts with expanding window...")
    forecasts = estimate_transitions(df)
    print(f"  Generated {len(forecasts)} forecasts")
    
    # Save to JSON
    print("\n[3/3] Saving forecast_data.json...")
    with open('forecast_data.json', 'w') as f:
        json.dump(forecasts, f, indent=2)
    
    print(f"\n✓ Saved {len(forecasts)} forecasts to forecast_data.json")
    
    # Show sample
    if len(forecasts) > 0:
        print("\nSample forecast (most recent):")
        sample = forecasts[-1]
        print(f"  Date: {sample['date']}")
        print(f"  Predicted: {sample['pred_state']} ({sample['confidence']:.1%} confidence)")
        print(f"  Top 3:")
        for i in range(1, 4):
            if sample[f'top{i}_state']:
                print(f"    {i}. {sample[f'top{i}_state']}: {sample[f'top{i}_prob']:.1%}")
    
    print("\n" + "="*80)
    print("COMPLETED")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
