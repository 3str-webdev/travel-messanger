import { Component } from '@angular/core';
import { Friend } from '../../types/models/friendModel'

@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.less']
})
export class UserPageComponent {
  images: string[] = new Array(20).fill('../../../assets/images/img-example.png')

  avatar: string = '../../../assets/aa1b8ce6570e33aa6b0bc0c475f2895e.jpg'
  firstName: string = 'Дмитрий'
  lastName: string = 'Щедрин'
  isOnline: boolean = true
  city: string = 'Санкт-Петербург'

  friends: Friend[] = new Array(135).fill({name: 'Серёжа', img: '../../../assets/images/img-example.png'})
  onlineFriends: Friend[] =  new Array(12).fill({name: 'Серёжа', img: '../../../assets/images/img-example.png'})
  friendsCount!: number
  onlineFriendsCount!: number
  firstFriends!: Friend[]
  firstOnlineFriends!: Friend[]
  constructor() {
    this.friendsCount = this.friends.length
    this.onlineFriendsCount = this.onlineFriends.length
    this.firstFriends = this.friends.slice(0, 8)
    this.firstOnlineFriends = this.onlineFriends.slice(0, 4)
  }
}
