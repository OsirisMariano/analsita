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
  
  // Validação de Dados: verificação dos dados de configuração do sistema
  dadosValidacao: {
    arquivos_validados_total: 30,
    status_geral: 'sucesso',
    validacoes: [
      {
        dado: 'codigoConveniado',
        valor: '02896',
        total_arquivos: 5,
        status: 'ok',
        arquivos: [
          { caminho_arquivo: '/etc/abastece/lado1/posto.json', dado: '02896', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado2/posto.json', dado: '02896', status: 'ok' },
          { caminho_arquivo: '/etc/hosts', dado: '028961', status: 'ok' },
          { caminho_arquivo: '/etc/hostname', dado: '028961', status: 'ok' },
          { caminho_arquivo: '/var/abastece/SLT/configpista/ifadapter.ini', dado: '02896', status: 'ok' }
        ]
      },
      {
        dado: 'config',
        valor: 'DS_ABAST.02896_1',
        total_arquivos: 1,
        status: 'ok',
        arquivos: [
          { caminho_arquivo: '/var/DS_SFTP/config.json', dado: 'DS_ABAST.02896_1', status: 'ok' }
        ]
      },
      {
        dado: 'IPs nuc',
        valor: '192.168.212.21',
        total_arquivos: 9,
        status: 'ok',
        arquivos: [
          { caminho_arquivo: '/etc/abastece/autorizador/retrofit-autorizador.json', dado: '192.168.212.21', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado1/antena.json', dado: '192.168.212.21', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado2/antena.json', dado: '192.168.212.21', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado1/camera.json', dado: '192.168.212.21 (pumatronix)', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado1/camera.json', dado: '192.168.212.21 (serverAddress)', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado1/camera.json', dado: '192.168.212.21 (cameraIP)', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado2/camera.json', dado: '192.168.212.21 (pumatronix)', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado2/camera.json', dado: '192.168.212.21 (serverAddress)', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado2/camera.json', dado: '192.168.212.21 (cameraIP)', status: 'ok' }
        ]
      },
      {
        dado: 'lane',
        valor: '1 / 2',
        total_arquivos: 6,
        status: 'ok',
        arquivos: [
          { caminho_arquivo: '/etc/abastece/lado1/antena.json', dado: '1', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado2/antena.json', dado: '2', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado1/posto.json', dado: '1', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado2/posto.json', dado: '2', status: 'ok' },
          { caminho_arquivo: '/var/abastece/forseti/config.json', dado: '1 - (lado 1)', status: 'ok' },
          { caminho_arquivo: '/var/abastece/forseti/config.json', dado: '2 - (lado 2)', status: 'ok' }
        ]
      },
      {
        dado: 'Portas Antena',
        valor: '51111',
        total_arquivos: 2,
        status: 'ok',
        arquivos: [
          { caminho_arquivo: '/etc/abastece/lado1/antena.json', dado: '51111', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado2/antena.json', dado: '51111', status: 'ok' }
        ]
      },
      {
        dado: 'Portas Camera',
        valor: '50041/50042',
        total_arquivos: 2,
        status: 'ok',
        arquivos: [
          { caminho_arquivo: '/etc/abastece/lado1/camera.json', dado: '50041', status: 'ok' },
          { caminho_arquivo: '/etc/abastece/lado2/camera.json', dado: '50042', status: 'ok' }
        ]
      },
      {
        dado: 'wtmp',
        valor: '7',
        total_arquivos: 4,
        status: 'ok',
        arquivos: [
          { caminho_arquivo: '/etc/logrotate.d/wtmp', dado: 'monthly (comentado)', status: 'ok' },
          { caminho_arquivo: '/etc/logrotate.d/wtmp', dado: 'daily (descomentado)', status: 'ok' },
          { caminho_arquivo: '/etc/logrotate.d/wtmp', dado: 'rotate 1 (comentado)', status: 'ok' },
          { caminho_arquivo: '/etc/logrotate.d/wtmp', dado: 'rotate 7 (descomentado)', status: 'ok' }
        ]
      },
      {
        dado: 'zabbix',
        valor: 'ativado',
        total_arquivos: 1,
        status: 'ok',
        arquivos: [
          { caminho_arquivo: '/etc/zabbix/zabbix_agent2.conf', dado: 'ativado', status: 'ok' }
        ]
      }
    ]
  },

  // Contador automático de erros para a Badge
  totalErros: computed(() => {
    return store.arquivos.filter(a => a.status === 'ERRO').length
  }),

  // Contador de erros na Validação de Dados (badge da sidebar)
  totalErrosDados: computed(() => {
    return store.dadosValidacao.validacoes.reduce(
      (acc, v) => acc + v.arquivos.filter(a => a.status !== 'ok').length,
      0
    )
  })
})