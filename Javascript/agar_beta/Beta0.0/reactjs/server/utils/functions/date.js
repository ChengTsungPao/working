const getLocalDate = () => {
    let datetime = new Date().toLocaleString('zh-TW', { timeZone: 'Asia/Taipei', hour12: false })
    let date = datetime.split(',')[0].split('/')
    let month = date[0]
    let day = date[1]
    let year = date[2]

    //if (day.length === 1) day = '0' + day;
    //if (month.length === 1) month = '0' + month;

    return `${year}-${month}-${day}`
}

module.exports = {
    'getLocalDate': getLocalDate
}