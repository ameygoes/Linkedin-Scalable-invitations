pipeline {
  agent any

  parameters {
    string(name: 'company', defaultValue: 'amazon', description: 'Company Name')
    choice(name: 'search_result_limit', choices: [25, 5, 10, 15, 20, 30, 50, 100], description: 'Search Result Limit')
    string(name: 'region', defaultValue: '103644278', description: 'Region')
    string(name: 'network_depths', defaultValue: 'S,O', description: 'Network Depths')
    choice(name: 'keyword_title', choices: ['Data Engineer', 'Data Analyst', 'Data Scientist', 'Data Architect', 'Data Manager', 'Recruiter', 'Technical Recruiter', 'Talent Acquisition Specialist'], description: 'Keyword Title')
  }

  stages {
    stage('Init') {
      steps {
        script {
          dir('D:/study-code-repeat/coding/Linkedin-Scalable-invitations') {
            // Read the contents of the runable_configs.py file
            def runable_configs = 'Configs/runable_configs.py'
            def fileContents = readFile(file: runable_configs).trim()

            // Extract the part after '='
            def environment = fileContents.split('=')[1].trim().replaceAll(/["']/, '').toLowerCase()

            // Compare the value with 'dev' or 'prod'
            def yamlFile
            if (environment == 'dev') {
              yamlFile = 'Params/test/jobParams.yaml'
            } else if (environment == 'prod') {
              yamlFile = 'Params/prod/jobParams.yaml'
            } else {
              error("Invalid environment value $value, Please check file: $runable_configs")
            }

            // Pass the yamlFile to the subsequent stages
            env.yamlFile = yamlFile
          }
        }
      }
    }

    stage('YAML Modification') {
      steps {
        dir('D:/study-code-repeat/coding/Linkedin-Scalable-invitations') {
          script {
            def yamlFile = env.yamlFile

            def yaml = readYaml file: yamlFile
            print(yaml)
            yaml.company = params.company
            yaml.search_result_limit = params.search_result_limit
            yaml.region = params.region
            yaml.network_depths = params.network_depths.split(',')
            yaml.keyword_title = params.keyword_title
            print(yaml)
            // Write the modified YAML back to the file
            writeYaml file: yamlFile, data: yaml
          }
        }
      }
    }

    stage('Run Python Files') {
      steps {
        dir('D:/study-code-repeat/coding/Linkedin-Scalable-invitations') {
          bat 'python Main\\save_people_to_db.py'
        }
      }
    }
  }
}
