<template>
  <div class="dashboard">
    <h1>📡 Analista SemParar - Dashboard</h1>
    <router-view />
  </div>
</template>

<style>
body {
  font-family: sans-serif;
  background-color: #1a1a1a;
  color: white;
  margin: 0;
  padding: 20px;
}
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}
</style>