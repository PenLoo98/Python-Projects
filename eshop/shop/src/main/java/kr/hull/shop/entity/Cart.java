package kr.hull.shop.entity;

import groovy.transform.ToString;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;


@Entity
@Table(name = "cart")
@Getter
@Setter
@ToString
public class Cart{

    @Id
    @Column(name = "cart_id")
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    //@OneToOne(fetch = FetchType.EAGER) //즉시 로딩 전략
    @OneToOne
    @JoinColumn(name="member_id")
    private Member member;

}