

async function requestRecent(){
  const response = await fetch(ApiUrl);
  const data = await response.json();
  console.log(data);
  return data;
}
