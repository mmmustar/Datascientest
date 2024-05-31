ENV['VAGRANT_DEFAULT_PROVIDER'] = 'docker' # Nous définissons le provider à utiliser qui est Docker, Début de l'instruction 1
Vagrant.configure("2") do |config| #Début de l'instruction 2
    config.vm.define "serveur_web" do |serveur_web| # Nous définissons un nom pour l'instance que nous devons paramétrer
    serveur_web.vm.network "forwarded_port", guest: 80, host: 9000, auto_correct: true # Nous demandons à ce que le port 9000 de l'hôte soit redirigé sur le port 80  du conteneur qui pourra être corrigé si le port 9000 est déjà alloué.
    serveur_web.vm.usable_port_range = (5000..5005) # Nous définissons la plage de ports qui sera utilisé dans le cas ou le port 9000 sera utilisé sur l'hôte
    serveur_web.vm.provider "docker" do |serveur_web| # Début de l'instruction 3
    serveur_web.image = "ubuntu:latest" # Nous définissons l'image docker à utiliser
    # admin.build_dir = "." # Nous pouvons également définir  l'emplacement du Dockerfile qui est le répertoire courant afin de construire notre image
    serveur_web.has_ssh = true # Connexion possible en SSH
    serveur_web.privileged = true # Exécutions du conteneur avec des privilègres sur la machine soujacente
    serveur_web.create_args = ["-v", "/sys/fs/cgroup:/sys/fs/cgroup:ro"] # Nous créons un volume qui connecte le répertoire des cgroup de notre hote sur celui de nos conteneurs
            serveur_web.name = "serveur_web_autocorrect" #Nous définissons un nom pour notre conteneur
   end  #Fin de l'instruction 3
  end  #Fin de l'instruction 2
end  #Fin de l'instruction 1