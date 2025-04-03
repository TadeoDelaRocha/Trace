<script lang="ts">
  import { goto } from '$app/navigation';
  import { loginAnalyst } from './loginLogic';

  // Local state for form fields and messages
  let initials: string = '';
  let isLead: boolean = false;
  let errorMessage: string = '';
  let successMessage: string = '';

  async function handleLogin() {
    // Reset messages
    errorMessage = '';
    successMessage = '';

    try {
      const response = await loginAnalyst(initials, isLead);
      successMessage = `Login successful! Role: ${response.analyst.role}`;
      // Optionally store the analyst info (e.g., in local storage)
      localStorage.setItem('user', JSON.stringify(response.analyst));
      // Redirect to the projects page after successful login
      goto('/projects/myProjects');
    } catch (error: any) {
      errorMessage = error.message || 'Login failed';
    }
  }
</script>

<style>
  /* Center the container */
  .login-container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background-color: #f0f2f5;
    padding: 1rem;
  }

  /* Style the form card */
  form {
    background: #fff;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 400px;
  }

  h1 {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #333;
  }

  form div {
    margin-bottom: 1rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #555;
  }

  input[type="text"] {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  input[type="checkbox"] {
    margin-right: 0.5rem;
    transform: scale(1.2);
  }

  button {
    width: 100%;
    padding: 0.75rem;
    background-color: #0070f3;
    border: none;
    border-radius: 4px;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    margin-top: 1rem;
  }

  button:hover {
    background-color: #005bb5;
  }

  p {
    text-align: center;
    margin-top: 1rem;
  }
</style>

<div class="login-container">
  <form on:submit|preventDefault={handleLogin}>
    <h1>Login</h1>
    
    <div>
      <label for="initials">Initials:</label>
      <input id="initials" type="text" bind:value={initials} required />
    </div>

    <div>
      <label for="isLead">
        <input id="isLead" type="checkbox" bind:checked={isLead} />
        Lead Analyst
      </label>
    </div>

    <button type="submit">Log In</button>

    {#if errorMessage}
      <p style="color: red;">{errorMessage}</p>
    {/if}

    {#if successMessage}
      <p style="color: green;">{successMessage}</p>
    {/if}
  </form>
</div>
