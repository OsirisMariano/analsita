import { reactive, computed } from 'vue'

export const store = reactive({
  // Lista completa de arquivos baseada na sua imagem
  arquivos: [
    { nome: 'posto.json: lado1', caminho: "'/etc/abastece/lado1/posto.json'", status: 'OK' },
    { nome: 'concentrador.json: lado1', caminho: "'/etc/abastece/lado1/concentrador.json'", status: 'OK' },
    { nome: 'sensor.json: lado1', caminho: "'/etc/abastece/lado1/sensor.json'", status: 'OK' },
    { nome: 'postoAberto: lado1', caminho: "'/etc/abastece/lado1/postoAberto.json'", status: 'OK' },
    { nome: 'posto.json: lado2', caminho: "'/etc/abastece/lado2/posto.json'", status: 'OK' },
    { nome: 'concentrador.json: lado2', caminho: "'/etc/abastece/lado2/concentrador.json'", status: 'OK' },
    { nome: 'sensor.json: lado2', caminho: "'/etc/abastece/lado2/sensor.json'", status: 'OK' },
    { nome: 'postoAberto: lado2', caminho: "'/etc/abastece/lado2/postoAberto.json'", status: 'OK' },
    { nome: 'hosts', caminho: "'/etc/hosts'", status: 'OK' },
    { nome: 'hostname', caminho: "'/etc/hostname'", status: 'OK' },
    { nome: 'ifadapter.ini', caminho: "'/var/abastece/SLT/configpista/ifadapter.ini'", status: 'OK' },
    { nome: 'Licença', caminho: "não existe em '/home/pi/vpar/licenca/*.V2C'", status: 'ERRO' }, // Erro detectado
    { nome: 'P12', caminho: "'/var/abastece/certificate/*.p12'", status: 'OK' },
    { nome: 'zabbix_agent2.conf', caminho: "'/etc/zabbix/zabbix_agent2.conf'", status: 'OK' },
    { nome: 'config.json', caminho: "'/var/DS_SFTP/config.json'", status: 'OK' }
  ],
  
  // Contador automático de erros para a Badge
  totalErros: computed(() => {
    return store.arquivos.filter(a => a.status === 'ERRO').length
  })
})