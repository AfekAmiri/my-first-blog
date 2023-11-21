from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import MoveForm
from .models import Pokemon,Lieu
from django.views.decorators.http import require_POST

def base(request):
    return render(request, 'blog/base.html', {})
def wiki_page(request):
    # pour afficher la page Wiki
    # Récupérer tous les types distincts
    types = Pokemon.objects.values_list('type', flat=True).distinct()
    # Créer un dictionnaire pour stocker les Pokémons par type
    pokemon_by_type = {type: Pokemon.objects.filter(type=type) for type in types}

    return render(request, 'blog/wiki.html', {'pokemon_by_type': pokemon_by_type})
def accueil_page(request):
    # pour afficher la page acceuil
    pokemons = Pokemon.objects.all()
    lieux = Lieu.objects.all()
    return render(request, 'blog/accueil.html', {'pokemons': pokemons, 'lieux': lieux})
'''def combat_page(request):
    # pour afficher la page acceuil
    pokemons = Pokemon.objects.filter(lieu='Parc')
    lieux = Lieu.objects.all()
    return render(request, 'blog/combat.html', {'pokemons': pokemons, 'lieux': lieux})'''
@require_POST 
def capturer(request,nom_pokemon):
    try:
        pokemon = Pokemon.objects.get(nom=nom_pokemon)
        
        if (pokemon.etat == 'Libre') and (pokemon.lieu == 'Parc'):
            pokemon.lieu = 'Ball'
            pokemon.etat = 'Affamé'
            pokemon.save()
            return render (request,'accueil',{'message': f"{pokemon.nom} a été capturé et est maintenant {pokemon.etat} dans la Ball."})
        else:
            return render(request,'accueil',{'message': f"Impossible de capturer {pokemon.nom}."})
    except Pokemon.DoesNotExist:
        return render(request,'accueil',{'message': f"Le Pokémon {nom_pokemon} n'existe pas."})
@require_POST 
def nourrir(request,nom_pokemon):
    try:
        # Nourrir le Pokémon s'il est affamé
        pokemon = Pokemon.objects.get(nom=nom_pokemon)
        
        # Vérifier si le Pokémon est affamé
        if (pokemon.etat == 'Affamé'):
            # Changer son état à Repus et son lieu à Restaurant
            pokemon.etat = 'Repus'
            pokemon.lieu = 'Restaurant'
            pokemon.save()
            return render(request,'accueil',{'message': f"{pokemon.nom} a été nourri et est maintenant {pokemon.etat} au Restaurant."})
        else:
            # Afficher un warning si l'opération est impossible
            return render(request,'accueil',{'message': f" {pokemon.nom} n'a pas faim"})
    except Pokemon.DoesNotExist:
        # Afficher un warning si le Pokémon n'existe pas
        return render (request,'accueil',{'message': f"Le Pokémon {nom_pokemon} n'existe pas."})

@require_POST 
def soigner(request,nom_pokemon):
    try:
        # Soigner le Pokémon s'il est blessé
        pokemon = Pokemon.objects.get(nom=nom_pokemon)
        infirmerie=Lieu.objects.get(id_lieu='Infirmerie')
        
        # Vérifier si le Pokémon est blessé et qu'il est au Parc
        if (pokemon.etat == 'Blessé') and (infirmerie.disponibilite=='Disponible'):
            # Changer son état à Affamé et son lieu à Infirmerie
            pokemon.etat = 'Affamé'
            pokemon.lieu = 'Infirmerie'
            infirmerie.disponibilite='Occupé'
            pokemon.save()
            return render(request,'accueil',{'message': f"{pokemon.nom} a été soigné et est maintenant {pokemon.etat} à l'Infirmerie."})
        else:
            # Afficher un warning box si l'opération est impossible
            return render (request,'accueil',{'message': f"{pokemon.nom} n'est pas blessé ou il est impossible de le soigner"})
    except Pokemon.DoesNotExist:
        # Afficher un warning box si le Pokémon n'existe pas
        return render (request,'accueil',{'message': f"Le Pokémon {nom_pokemon} n'existe pas."})
@require_POST     
def divertir(request,nom_pokemon):
    try:
        # Divertir le Pokémon s'il est repus
        pokemon = Pokemon.objects.get(nom=nom_pokemon)
        parc=Lieu.objects.get(id_lieu="Parc")
        
        # Vérifier si le Pokémon est repus et que le parc est disponible
        if (pokemon.etat == 'Repus') and(parc.disponibilite=="Disponible") :
            # Changer son état à Libre et son lieu à Parc
            pokemon.etat = 'Libre'
            pokemon.lieu = 'Parc'
            if len(Lieu.objects.get(id_lieu="Parc").get_occupants())==2:
                parc.disponibilite="Occupé"
            pokemon.save()
            return render(request,'accueil',{'message': f"{pokemon.nom} a été diverti et est maintenant {pokemon.etat} au Parc."})
        else:
            # Afficher un warning box si l'opération est impossible
            return render (request,'accueil',{'message': f"{pokemon.nom} n'est pas repus ou le parc est occupé"})
    except Pokemon.DoesNotExist:
        # Afficher un warning box si le Pokémon n'existe pas
        return render (request,'accueil',{'message': f"Le Pokémon {nom_pokemon} n'existe pas."})
'''def vainqueur(type1, type2):
    # Logique de détermination du vainqueur basée sur les types
    if type1 == 'Feu' and type2 == 'Plante':
        return 1  # Pokémon de type Feu gagne contre Plante
    elif type1 == 'Eau' and type2 == 'Feu':
        return 1  # Pokémon de type Eau gagne contre Feu
    elif type1 == 'Sol' and type2 == 'Eau':
        return 1  # Pokémon de type Sol gagne contre Eau
    elif type1 == 'Plante' and type2 == 'Sol':
        return 1  # Pokémon de type Plante gagne contre Sol
    elif type1 == 'Sol' and type2 == 'Feu':
        return 1  # Pokémon de type Sol gagne contre Feu
    elif type1 == 'Eau' and type2 == 'Plante':
        return 1  # Pokémon de type Eau gagne contre Plante
    else:
        return 2  # Si aucune condition n'est remplie, le Pokémon 2 gagne
def combat(request, nom_pokemon1,nom_pokemon2):
    try:
        #faire un combat
        pokemon1 = Pokemon.objects.get(nom=nom_pokemon1)
        pokemon2 = Pokemon.objects.get(nom=nom_pokemon2)
        # Vérifier si les deux pokemons ne sont pas blessés
        if (pokemon1.etat != 'Blessé') and(pokemon1.etat != 'Blessé') :
            #Déterminer le gagnant
            niveau1=pokemon1.niveau
            niveau2=pokemon2.niveau
            type1=pokemon1.type
            type2=pokemon2.type
            Niveaux={'Faible':1,'Moyen':2,'Fort':3}
            if Niveaux[niveau1]>Niveaux[niveau2]:
                gagnant=pokemon1
                pokemon2.etat='Blessé'
            elif Niveaux[niveau2]>Niveaux[niveau1]:
                gagnant=pokemon2
                pokemon1.etat='Blessé'
            else:
                winner=vainqueur(type1, type2)
                if (winner==1):
                    gagnant=pokemon1
                    pokemon2.etat='Blessé'
                else:
                    gagnant=pokemon2
                    pokemon1.etat='Blessé'
            pokemon1.save()
            pokemon2.save()
            return render(request, 'combat.html', {'winner': gagnant})
        else:
            # Afficher un warning box si l'opération est impossible
            return render(request, 'blog/warning_box.html', {'message': f"Le pokémon {Pokemon.objects.filter(lieu='Parc',etat='Blessé').first().nom} est blessé"})
    except Pokemon.DoesNotExist:
        # Afficher un warning box si le Pokémon n'existe pas
        return render(request, 'blog/warning_box.html', {'message': f"not found"})'''
@csrf_exempt
@require_POST 
def accueil_action(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        nom = request.POST.get('nom')
        
        # Obtenez le Pokémon spécifique par ID
        pokemon = Pokemon.objects.get(nom=nom)
        
        # Logique pour les différentes actions (capture, nourrir, divertir)
        if action == 'capturer':
            capturer(request,pokemon)
        elif action == 'nourrir':
            nourrir(request,pokemon)
        elif action == 'divertir':
            divertir(request,pokemon)
        elif action == 'soigner':
            soigner(request,pokemon)
        return JsonResponse({'success': True, 'message': f"{pokemon.nom} est maintenant {pokemon.etat} et est dans {pokemon.lieu}"})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

def pokemon_detail(request, nom):
    pokemon = get_object_or_404(Pokemon , nom=nom)
    lieu = pokemon.lieu
    form=MoveForm(request.POST, instance=pokemon)
    if form.is_valid():
        ancien_lieu = get_object_or_404(Lieu, id_lieu=pokemon.lieu.id_lieu)
        nouveau_lieu_id = form.cleaned_data['lieu']
        nouveau_lieu = get_object_or_404(Lieu, id_lieu=nouveau_lieu_id)
        if nouveau_lieu.id_lieu == 'Infirmerie' and nouveau_lieu.disponibilite=='Occupé':
            return render(request, 'blog/pokemon_detail.html', {'pokemon': pokemon, 'lieu': lieu, 'form': form, 'error_message': 'L\'infirmerie est pleine.'})
        elif nouveau_lieu.id_lieu == 'Parc' and len(nouveau_lieu.get_occupants())==2:
            return render(request, 'blog/pokemon_detail.html', {'pokemon': pokemon, 'lieu': lieu, 'form': form, 'error_message': 'Le parc est plein.'})
        else:
            ancien_lieu.disponibilite = "Libre"
            ancien_lieu.save()
            form.save(commit=False)
            nouveau_lieu.disponibilite = "Occupé"
            nouveau_lieu.save()
            id=nouveau_lieu.id_lieu
            if (id=='Restaurant'):
                pokemon.etat='Repus'
            elif ((id=='Ball') or (id=='Infirmerie')):
                pokemon.etat='Affamé'
            elif (id=='parc'):
                pokemon.etat='Libre'
            pokemon.lieu=nouveau_lieu
            pokemon.save()
            return redirect('pokemon_detail',nom=nom)
    else:
        form = MoveForm()
        return render(request,
                  'blog/pokemon_detail.html',
                  {'pokemon': pokemon, 'lieu': lieu, 'form': form})
