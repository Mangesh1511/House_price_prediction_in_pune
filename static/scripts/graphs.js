const site_location=[];
const total_sqft=[];
const bath=[];
const bhk=[] ;
const price=[];

  
async function charData(){
  const datapoints = await d3.csv('Cleaned_data.csv');
  for(i=0;i<datapoints.length;i++)
  {
      price.push(datapoints[i].price)
      site_location.push(datapoints[i].site_location)
      total_sqft.push(datapoints[i].total_sqft)
      bath.push(datapoints[i].bath)
      bhk.push(datapoints[i].consolebhk)
  }
}
const myChart = document.getElementById("myChart");
let pointBackgroundColors = [];
    let ie1LineChart = new Chart(myChart{
        type: 'line',
        data: {
            labels: site_loaction,
            datasets : [
                {
                    label : 'site_location',
                    data : site_location,
                    fill: false,
                    borderColor: 'rgb(75,192,192)',
                    tension: 0.3,
                    pointBackgroundColor: pointBackgroundColors
                }
            ]

        }
     })

     for (let i = 0; i < site_location.length; i++) 
    {
        let bg = myChart.data.datasets[0].pointBackgroundColor;
        if(ie1[i]<4)
        {
            pointBackgroundColors.push("rgb(255,0,0)");
            
        }
        else{
            pointBackgroundColors.push("rgb(0,122,0)");
        }
    }
    ie1LineChart.update();







            
            