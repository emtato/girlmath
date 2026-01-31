# Stars & Constellations Database Documentation

## Overview
This system implements a learning tracker where journal entries are analyzed to extract topics (stars) which are organized into subject categories (constellations).

## Collections Schema

### stars (Topics)
```javascript
{
  _id: ObjectId,
  user_id: String,              // Owner
  name: String,                 // Normalized topic name
  constellation_id: String,     // Parent constellation
  journal_ids: [String],        // Referenced journals
  created_at: DateTime
}
```

### constellations (Categories)
```javascript
{
  _id: ObjectId,
  name: String,
  description: String,
  is_global: Boolean,           // System-wide or user-specific
  user_id: String,              // If user-specific
  created_at: DateTime
}
```

### journals (Updated)
```javascript
{
  // ... existing fields ...
  star_ids: [String]            // Linked stars
}
```

## Relationships
```
Journal *---* Star *---1 Constellation
     (references)  (belongs to)
```

Bidirectional: `star.journal_ids[]` ↔ `journal.star_ids[]`

## Key Functions

### star_crud.py
- `create_star(user_id, name, constellation_id)`
- `get_star_by_name(user_id, name)`
- `link_star_to_journal(star_id, journal_id)` - Bidirectional
- `get_journals_for_star(star_id)`

### constellation_crud.py
- `create_constellation(name, description, is_global, user_id)`
- `get_constellation_with_stars(constellation_id, user_id)` - Aggregation
- `get_all_constellations(user_id, include_stars)`

### analyze_and_link_stars.py
- `analyze_and_link_stars(user_id, journal_id, text)` - AI extraction
- `get_constellation_map(user_id)` - Hierarchical view
- `expand_star_to_journals(star_id)` - Show all journals for topic

## Usage Example

```python
# Analyze journal and link topics
result = await analyze_and_link_stars(
    user_id="user123",
    journal_id="journal456",
    journal_text="Learned about neural networks..."
)

# View constellation map
map_data = await get_constellation_map(user_id="user123")

# Expand topic to see all journals
result = await expand_star_to_journals(star_id="star789")
```

## Setup
Run: `python db/setup_indexes.py` to create indexes
