# User Settings Form Schema

This document describes the JSON structure sent by the frontend `UserSettingsForm` to the `/api/setUserInfo` endpoint. Generated with gemini ai

## JSON Structure

```json
{
  "username": "string",
  "completedClasses": [
    {
      "className": "string",
      "grade": "string",
      "difficulty": number
    }
  ],
  "strengths": {
    "Math": number,
    "Algorithms": number,
    "Data Structures": number,
    "Programming": number,
    "Recursion": number
  },
  "specialization": "string",
  "quartersLeft": number
}
```

## Field Descriptions

| Field | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` | The unique identifier for the user (retrieved from cookies). |
| `completedClasses` | `array` | A list of objects representing courses the student has already finished. |
| `completedClasses[].className` | `string` | The ID of the course (e.g., "CS 161"). |
| `completedClasses[].grade` | `string` | The grade received in the course (e.g., "A", "B+", "P"). |
| `completedClasses[].difficulty` | `number` | A self-reported difficulty rating from 1 to 5. |
| `strengths` | `object` | An object containing self-assessment scores for various core topics. |
| `strengths[TOPIC]` | `number` | A score from 1 (weakest) to 5 (strongest). Topics include Math, Algorithms, Data Structures, Programming, and Recursion. |
| `specialization` | `string` | The student's chosen CS specialization (e.g., "AI", "Algorithms"). |
| `quartersLeft` | `number` | The number of quarters remaining until graduation. |

## Example Payload

```json
{
  "username": "nathan",
  "completedClasses": [
    {
      "className": "I&CSCI 31",
      "grade": "A",
      "difficulty": 2
    },
    {
      "className": "I&CSCI 32",
      "grade": "B+",
      "difficulty": 4
    }
  ],
  "strengths": {
    "Math": 4,
    "Algorithms": 3,
    "Data Structures": 5,
    "Programming": 5,
    "Recursion": 4
  },
  "specialization": "Algorithms",
  "quartersLeft": 6
}
```
