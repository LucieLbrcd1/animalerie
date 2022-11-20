from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal
from .models import Equipement

# Create your views here.

def animal_list(request):
    animals = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'animalerie/animal_list.html', {"animals" : animals, "equipements" : equipements} )

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    equipements = Equipement.objects.all()
    mangeoire = get_object_or_404(Equipement, id_equip='mangeoire')
    roue = get_object_or_404(Equipement, id_equip='roue')
    nid = get_object_or_404(Equipement, id_equip='nid')
    litiere = get_object_or_404(Equipement, id_equip='litiere')
    animal = get_object_or_404(Animal, id_animal=id_animal)
    formerlieu = get_object_or_404(Equipement, id_equip=animal.lieu)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
        if form.is_valid():
            if form.data['lieu'] == 'mangeoire':
                if mangeoire.disponibilite == 'occupe':
                    return render(request ,"animalerie/animal_detail.html", {'animal': animal, 'message': "Impossible , la mangeoire est déjà occupé !" , 'equipements': equipements})
                elif animal.etat == 'affame' and mangeoire.disponibilite == 'libre':
                    formerlieu.disponibilite = "libre"
                    formerlieu.save()
                    animal.etat = 'repus'
                    form.save()                  
                    newlieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    newlieu.disponibilite = "occupe"
                    new.save()
                    animal.save()
                    return redirect('animal_list')      
                else:
                    if formerlieu!= litiere:
                        formerlieu.disponibilite = "occupe"
                        formerlieu.save()
                        form.save(commit=False)
                    return render(request ,"animalerie/animal_detail.html", {'animal': animal, 'message': f"Malheureusement {animal} n'a pas faim !",'equipements': equipements})    
            elif form.data['lieu'] == 'roue':
                if roue.disponibilite == 'occupe':
                    return render(request ,"animalerie/animal_detail.html", {'animal': animal, 'message': f"Impossible , la roue est déjà occupé !",'equipements': equipements})            
                elif animal.etat == 'repus' and roue.disponibilite == 'libre':
                    formerlieu.disponibilite = "libre"
                    formerlieu.save()
                    animal.etat = 'fatigue'
                    form.save()
                    newlieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    newlieu.disponibilite = "occupe"
                    newlieu.save()
                    animal.save()
                    return redirect('animal_list')   
                else:
                    if formerlieu!= litiere:
                        formerlieu.disponibilite = "occupe"
                        formerlieu.save()
                        form.save(commit=False)
                    return render(request ,"animalerie/animal_detail.html", {'animal': animal, 'message': f"Malheureusement {animal} n'a pas assez mangé !",'equipements': equipements})
            elif form.data['lieu'] == 'nid':
                if nid.disponibilite == 'occupe':
                    return render(request ,"animalerie/animal_detail.html", {'animal': animal, 'message': f"Impossible , le nid est déjà occupé !",'equipements': equipements})            
                elif animal.etat == 'fatigue' and nid.disponibilite == 'libre':
                    formerlieu.disponibilite = "libre"
                    formerlieu.save()
                    animal.etat = 'endormi'
                    form.save()
                    formerlieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    newlieu.disponibilite = "occupe"
                    newlieu.save()
                    animal.save()
                    return redirect('animal_list')                       
                else:
                    if formerlieu!= litiere:
                        formerlieu.disponibilite = "occupe"
                        formerlieu.save()
                        form.save(commit=False)
                    return render(request ,"animalerie/animal_detail.html", {'animal': animal, 'message': f"Malheureusement {animal} n'est pas fatigué !",'equipements': equipements})
            elif form.data['lieu'] == 'litiere':
                if litiere.disponibilite == 'occupe':
                    return render(request ,"animalerie/animal_detail.html", {'animal': animal, 'message': f"Impossible , la litière est déjà occupé !",'equipements': equipements})              
                elif animal.etat == 'endormi' and litiere.disponibilite == 'libre':
                    former.disponibilite = "libre"
                    former.save()
                    animal.etat = 'affame'
                    form.save()
                    newlieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    newlieu.disponibilite = "libre"
                    newlieu.save()
                    animal.save()
                    return redirect('animal_list')                      
                else:
                    if formerlieu!= litiere:
                        formerlieu.disponibilite = "occupe"
                        formerlieu.save()
                        form.save(commit=False)
                    return render(request ,"animalerie/animal_detail.html", {'animal': animal, 'message': f"Malheureusement {animal} ne dors pas !",'equipements': equipements})

        else:
            form = MoveForm()
    else:
        form = MoveForm()

    return render(request, 'animalerie/animal_detail.html', {'animal': animal, 'lieu': animal.lieu, 'form': form,'equipements': equipements})

def equipement_detail(request, id_equip):
    equipement = get_object_or_404(Equipement, id_equip=id_equip)
    animaux = Animal.objects.all()
    for animal in animaux:
        if animal.lieu == equipement:
            return render(request, 'animalerie/equipement_detail.html', {"equipement" : equipement, "animal": animal})        
    return render(request, 'animalerie/equipement_detail.html', {"equipement" : equipement})
 
