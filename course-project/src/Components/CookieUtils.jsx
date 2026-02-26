// simple cookie reader written by gemini ai
export function ReadCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

export function SetCookie(name, value){
  document.cookie = `${name}=${value}; path=/; max-age=3600; SameSite=Lax`;
}
