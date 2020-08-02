
    let img = document.querySelector('.img-fluid')
    let category = document.querySelector('#categ').getAttribute('value')
    
    console.log(category)

    
    if (category == "1")
    {
        img.src= "/static/images/essencial_oil.jpg"
    }
    else if (category == 2)
    {
        img.src = "/static/images/tea.jpg"
    }else if (category == 3){
        img.src = "/static/images/flowerHeart.jpg"
    }else if (category == 4){
        img.src = "/static/images/plant.jpg"

    }else{
        img.src= "/static/images/garden.jpg"
    
    }



