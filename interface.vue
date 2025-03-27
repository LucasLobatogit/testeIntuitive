<template>
  <div id="app" class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Busca de Operadoras</h1>
    
    <div class="flex mb-4">
      <input 
        v-model="searchQuery" 
        @keyup.enter="buscarOperadoras"
        type="text" 
        placeholder="Digite sua busca..."
        class="flex-grow p-2 border rounded-l-lg"
      >
      <button 
        @click="buscarOperadoras"
        class="bg-blue-500 text-white px-4 py-2 rounded-r-lg"
      >
        Buscar
      </button>
    </div>

    <div v-if="loading" class="text-center">
      Carregando...
    </div>

    <div v-if="resultados.length > 0">
      <p class="mb-2">Total de resultados: {{ total }}</p>
      
      <table class="w-full border-collapse">
        <thead>
          <tr class="bg-gray-200">
            <th class="border p-2">Registro</th>
            <th class="border p-2">Nome</th>
            <th class="border p-2">CNPJ</th>
            <th class="border p-2">Relevância</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="(operadora, index) in resultados" 
            :key="index" 
            class="hover:bg-gray-100"
          >
            <td class="border p-2">{{ operadora.Registro }}</td>
            <td class="border p-2">{{ operadora.Nome }}</td>
            <td class="border p-2">{{ operadora.CNPJ }}</td>
            <td class="border p-2">{{ operadora.relevancia }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!loading && resultados.length === 0" class="text-center text-gray-500">
      Nenhum resultado encontrado.
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      searchQuery: '',
      resultados: [],
      total: 0,
      loading: false
    }
  },
  methods: {
    async buscarOperadoras() {
      if (!this.searchQuery.trim()) {
        alert('Por favor, digite um termo de busca')
        return
      }

      this.loading = true
      this.resultados = []

      try {
        const response = await axios.get('http://localhost:5000/search', {
          params: { query: this.searchQuery }
        })

        this.resultados = response.data.resultados
        this.total = response.data.total
      } catch (error) {
        console.error('Erro na busca:', error)
        alert('Erro ao buscar operadoras')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
