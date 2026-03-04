export function cleanCourseName(course) {
  if (course) {
    // Matches "I&C SCI", "I&CSCI", etc. and replaces with "ICS "
    return course.replace(/I&C\s*SCI/g, "ICS ").replace(/COMPSCI/g, "CS ");
  }
}
